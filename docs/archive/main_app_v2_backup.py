import customtkinter as ctk
from tkinter import filedialog, END
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
import tensorflow as tf
import threading
import requests
from datetime import datetime
import time

# Local Imports
try:
    from resource_helper import resource_path
except:
    resource_path = lambda x: x

try:
    from chatbot_logic import AquaBot
except:
    class AquaBot:
        def check_status(self): return False
        def chat(self, msg): return "Chatbot not available"

try:
    from disease_info import DISEASE_INFO
except:
    DISEASE_INFO = {}

try:
    from fish_species_info import FISH_SPECIES_INFO, get_species_info
except:
    FISH_SPECIES_INFO = {}
    get_species_info = lambda x: None

# New Professional Features
try:
    from database import get_database
    from alert_system import get_alert_system
    from multi_fish_detector import get_multi_fish_detector
    from gradcam import GradCAM
    PROFESSIONAL_FEATURES = True
except Exception as e:
    print(f"Professional features not available: {e}")
    PROFESSIONAL_FEATURES = False

# --- Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AquaVisionPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("AquaVision AI")
        self.geometry("1280x800")
        self.minsize(1024, 768)

        # Initialize variables
        self.aquabot = AquaBot()
        self.species_model = None
        self.disease_model = None
        self.species_classes = None
        self.disease_classes = None
        self.models_loaded = False
        self.camera_active = False
        self.video_active = False
        self.cap = None
        self.frame_count = 0
        self.current_video_path = None
        self.current_image = None
        
        #  Professional Features
        if PROFESSIONAL_FEATURES:
            self.db = get_database()
            self.alerts = get_alert_system()
            self.multi_fish_detector = None
            self.gradcam = None
            self.gradcam_enabled = False
            self.multi_fish_mode = False
        else:
            self.db = None
            self.alerts = None

        # Configure Main Grid Layout
        self.grid_columnconfigure(0, weight=3, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        self.grid_rowconfigure(0, weight=1)

        # ================= MAIN CONTENT FRAME (LEFT) =================
        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        
        self.main_content_frame.grid_rowconfigure(2, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # --- 1. Header ---
        self.header_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.logo_label = ctk.CTkLabel(self.header_frame, text="🐟", font=ctk.CTkFont(size=30))
        self.logo_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(self.header_frame, text="AquaVision AI", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(side="left", anchor="s")
        
        subtitle_label = ctk.CTkLabel(self.header_frame, text=" Fish Health Analysis System", text_color="gray")
        subtitle_label.pack(side="left", anchor="s", padx=10, pady=(5,0))
        
        # Status indicators on right
        self.model_status = ctk.CTkLabel(self.header_frame, text="⚙️ Loading...", 
                                        font=ctk.CTkFont(size=11), text_color="orange")
        self.model_status.pack(side="right", padx=15)

        # --- 2. Control Buttons ---
        self.buttons_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="btns")

        btn_config = {"height": 45, "corner_radius": 8, "font": ctk.CTkFont(weight="bold")}
        
        self.btn_image = ctk.CTkButton(self.buttons_frame, text="🖼️ Image", 
                                       command=self.browse_image, **btn_config)
        self.btn_image.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_video = ctk.CTkButton(self.buttons_frame, text="🎥 Video", 
                                       command=self.toggle_video, **btn_config)
        self.btn_video.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.btn_camera = ctk.CTkButton(self.buttons_frame, text="📷 Camera", 
                                        command=self.toggle_camera, **btn_config, 
                                        fg_color="#00c853", hover_color="#009624")
        self.btn_camera.grid(row=0, column=2, padx=5, sticky="ew")
        
        self.btn_analyze = ctk.CTkButton(self.buttons_frame, text="🔍 Analyze", 
                                         command=self.quick_analyze, **btn_config, 
                                         fg_color="#00b0ff", hover_color="#0091ea")
        self.btn_analyze.grid(row=0, column=3, padx=(5, 0), sticky="ew")

        # --- 3. Main Display Area ---
        self.display_frame = ctk.CTkFrame(self.main_content_frame, corner_radius=15, fg_color="#151521")
        self.display_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        
        self.display_label = ctk.CTkLabel(self.display_frame, text="", fg_color="#151521")
        self.display_label.pack(fill="both", expand=True)
        
        self.placeholder_label = ctk.CTkLabel(self.display_label, 
                                             text="📸\n\nUpload image/video or start camera", 
                                             font=ctk.CTkFont(size=18), text_color="gray")
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- 4. Status Panels ---
        self.status_panel_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.status_panel_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        self.status_panel_frame.grid_columnconfigure((0, 1), weight=1, uniform="panels")

        # Species Detected Panel
        self.species_frame = ctk.CTkFrame(self.status_panel_frame, corner_radius=10)
        self.species_frame.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ctk.CTkLabel(self.species_frame, text="🐟 SPECIES DETECTED", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5))
        self.species_label = ctk.CTkLabel(self.species_frame, text="—", 
                                         font=ctk.CTkFont(size=20, weight="bold"),
                                         text_color="#00b0ff")
        self.species_label.pack(pady=(0, 15))

        # Health Status Panel
        self.health_frame = ctk.CTkFrame(self.status_panel_frame, corner_radius=10)
        self.health_frame.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        ctk.CTkLabel(self.health_frame, text="🏥 HEALTH STATUS", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5))
        self.disease_label = ctk.CTkLabel(self.health_frame, text="—", 
                                         font=ctk.CTkFont(size=20, weight="bold"),
                                         text_color="#00c853")
        self.disease_label.pack(pady=(0, 15))

        # --- 5. Footer Information ---
        self.footer_frame = ctk.CTkFrame(self.main_content_frame, corner_radius=10)
        self.footer_frame.grid(row=4, column=0, sticky="nsew")
        self.footer_frame.grid_rowconfigure(1, weight=1)
        self.footer_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.footer_frame, text="📋 TREATMENT & SPECIES INFORMATION", 
                    font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", 
                                                           padx=20, pady=(15, 5))
        
        self.remedy_box = ctk.CTkTextbox(self.footer_frame, height=120, 
                                        fg_color="#0d1117",
                                        font=ctk.CTkFont(size=12),
                                        wrap="word")
        self.remedy_box.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.remedy_box.insert("0.0", "Awaiting analysis...")
        self.remedy_box.configure(state="disabled")

        # ================= SIDEBAR FRAME (RIGHT) =================
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a2e")
        self.sidebar_frame.grid(row=0, column=1, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        # --- Status Indicators ---
        self.status_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.status_frame.pack(fill="x", padx=20, pady=30)
        
        self.ai_status = ctk.CTkLabel(self.status_frame, text="● AI Offline", 
                                     text_color="gray", font=ctk.CTkFont(weight="bold"))
        self.ai_status.pack(side="left")
        
        self.ready_status = ctk.CTkLabel(self.status_frame, text="○ Standby", 
                                        text_color="gray", font=ctk.CTkFont(weight="bold"))
        self.ready_status.pack(side="right")

        # --- 1. AI Assistant ---
        ctk.CTkLabel(self.sidebar_frame, text="🤖 AI Assistant", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=20, pady=(0, 15))
        
        self.chat_frame = ctk.CTkFrame(self.sidebar_frame, corner_radius=15, fg_color="#2b2b42")
        self.chat_frame.pack(fill="x", padx=20, pady=(0, 30))

        # Chat History
        self.chat_history = ctk.CTkTextbox(self.chat_frame, height=150, fg_color="transparent", 
                                          text_color="white", wrap="word")
        self.chat_history.pack(fill="both", expand=True, padx=15, pady=(15, 0))
        self.chat_history.insert("0.0", "🤖 Hello! I'm your AquaVision assistant. Ask me anything about fish care or disease identification.\n\n")
        self.chat_history.configure(state="disabled")

        # Chat Input Area
        self.input_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=15, pady=15)
        
        self.chat_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ask about fish care, disease...", 
                                      height=40, corner_radius=20, border_width=0, fg_color="#3f3f5f")
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.chat_entry.bind("<Return>", self.send_message)
        
        self.send_btn = ctk.CTkButton(self.input_frame, text="→", width=45, height=45, 
                                     corner_radius=20, font=ctk.CTkFont(size=20), 
                                     command=self.send_message,
                                     fg_color="#00b0ff", hover_color="#0091ea")
        self.send_btn.pack(side="right")

        # --- 2. Latest News ---
        ctk.CTkLabel(self.sidebar_frame, text="📰 Latest News", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=20, pady=(0, 15))
        
        self.news_scroll_frame = ctk.CTkScrollableFrame(self.sidebar_frame, corner_radius=15, 
                                                        fg_color="transparent")
        self.news_scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Start background tasks
        threading.Thread(target=self.load_models, daemon=True).start()
        threading.Thread(target=self.load_news, daemon=True).start()
        threading.Thread(target=self.check_ai_status, daemon=True).start()

    def check_ai_status(self):
        if self.aquabot.check_status():
            self.ai_status.configure(text="●AI Online", text_color="#00e676")
        else:
            self.ai_status.configure(text="○ AI Offline", text_color="gray")

    def load_models(self):
        try:
            model_loaded = False
            if os.path.exists(os.path.join("models", "species_model_fixed.h5")):
                try:
                    self.species_model = tf.keras.models.load_model(
                        os.path.join("models", "species_model_fixed.h5"), compile=False)
                    self.disease_model = tf.keras.models.load_model(
                        os.path.join("models", "disease_model_fixed.h5"), compile=False)
                    model_loaded = True
                except:
                    pass
            
            if model_loaded and hasattr(self.species_model, 'predict'):
                try:
                    test_input = np.random.random((1, 224, 224, 3)).astype(np.float32)
                    _ = self.species_model.predict(test_input, verbose=0)
                except:
                    model_loaded = False
            else:
                model_loaded = False
            
            if model_loaded:
                if os.path.exists(os.path.join("models", "species_classes.txt")):
                    with open(os.path.join("models", "species_classes.txt"), 'r') as f:
                        self.species_classes = [line.strip() for line in f if line.strip()]
                else:
                    self.species_classes = ["Sea Bass", "Tuna", "Salmon", "Goldfish", "Koi", 
                                          "Catfish", "Trout", "Tilapia", "Carp"]
                
                if os.path.exists(os.path.join("models", "disease_classes.txt")):
                    with open(os.path.join("models", "disease_classes.txt"), 'r') as f:
                        self.disease_classes = [line.strip() for line in f if line.strip()]
                else:
                    self.disease_classes = ["Healthy Fish", "Bacterial Infection", "Fungal Disease",
                                          "Parasitic Infection", "Viral Disease"]
                self.models_loaded = True
                self.model_status.configure(text="✅ Ready", text_color="#00e676")
                self.ready_status.configure(text="✓ Ready", text_color="#00e676")
            else:
                self.models_loaded = False
                self.model_status.configure(text="⚠️ Demo Mode", text_color="#ffd60a")
                self.species_classes = ["Sea Bass", "Goldfish", "Tuna", "Salmon", "Koi", "Catfish"]
                self.disease_classes = ["Healthy Fish", "Bacterial Infection", "Parasitic Infection"]
                self.species_model = None
                self.disease_model = None
        except Exception as e:
            self.model_status.configure(text="⚠️ Demo Mode", text_color="#ffd60a")
            self.models_loaded = False
            self.species_model = None
            self.disease_model = None
            self.species_classes = ["Sea Bass", "Goldfish", "Tuna"]
            self.disease_classes = ["Healthy Fish", "Needs Checkup"]

    def load_news(self):
        try:
            response = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    'q': 'fisheries OR aquaculture',
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 5,
                    'apiKey': 'd5b5b238be9547be9d816f7153f98300'
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                for article in data.get('articles',  [])[:5]:
                    self._add_news_card(
                        title=article.get('title', '')[:60],
                        source=article.get('source', {}).get('name', ''),
                        date=article.get('publishedAt', '')[:10],
                        url=article.get('url', '')
                    )
        except:
            # Fallback news
            news_data = [
                ("Latest aquaculture trends in India", "Fish News", "2025-12-05", "https://www.google.com/search?q=aquaculture+trends+india"),
                ("New disease detection methods", "Research Today", "2025-12-04", "https://www.google.com/search?q=fish+disease+detection"),
                ("Sustainable fishing practices", "Ocean Magazine", "2025-12-03", "https://www.google.com/search?q=sustainable+fishing"),
            ]
            for title, source, date, url in news_data:
                self._add_news_card(title, source, date, url)
    
    def _add_news_card(self, title, source, date, url=""):
        """Add a styled clickable news card"""
        import webbrowser
        
        try:
            news_date = datetime.strptime(date, "%Y-%m-%d")
            days_ago = (datetime.now() - news_date).days
            if days_ago == 0:
                time_ago = "Today"
            elif days_ago == 1:
                time_ago = "1 day ago"
            else:
                time_ago = f"{days_ago} days ago"
        except:
            time_ago = date
        
        news_item_frame = ctk.CTkFrame(self.news_scroll_frame, corner_radius=10, 
                                      fg_color="#2b2b42", border_width=1, border_color="#3f3f5f")
        news_item_frame.pack(fill="x", pady=(0, 10))
        
        def open_url(event=None):
            if url:
                webbrowser.open(url)
        
        def on_enter(event):
            news_item_frame.configure(fg_color="#3a3a52", cursor="hand2")
        
        def on_leave(event):
            news_item_frame.configure(fg_color="#2b2b42")
        
        news_item_frame.bind("<Button-1>", open_url)
        news_item_frame.bind("<Enter>", on_enter)
        news_item_frame.bind("<Leave>", on_leave)
        
        title_label = ctk.CTkLabel(news_item_frame, text=f"📌 {title}", 
                                   font=ctk.CTkFont(weight="bold"), anchor="w")
        title_label.pack(fill="x", padx=15, pady=(10, 0))
        title_label.bind("<Button-1>", open_url)
        title_label.bind("<Enter>", on_enter)
        title_label.bind("<Leave>", on_leave)
        
        meta_label = ctk.CTkLabel(news_item_frame, text=f"{source} • {time_ago}", 
                                 text_color="gray", font=ctk.CTkFont(size=11), anchor="w")
        meta_label.pack(fill="x", padx=15, pady=(0, 10))
        meta_label.bind("<Button-1>", open_url)
        meta_label.bind("<Enter>", on_enter)
        meta_label.bind("<Leave>", on_leave)

    def toggle_camera(self):
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()

    def start_camera(self):
        if hasattr(self, 'placeholder_label') and self.placeholder_label.winfo_exists():
            self.placeholder_label.place_forget()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return
        
        self.stop_video()
        self.camera_active = True
        self.btn_camera.configure(text="⏹ Stop Camera", fg_color="#ef476f")
        threading.Thread(target=self.camera_loop, daemon=True).start()

    def stop_camera(self):
        self.camera_active = False
        if self.cap:
            self.cap.release()
        self.btn_camera.configure(text="📷 Camera", fg_color="#00c853")

    def camera_loop(self):
        while self.camera_active:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img.thumbnail((800, 600))
            
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.display_label.configure(image=photo)
            self.display_label.image = photo
            
            if self.models_loaded:
                self.frame_count += 1
                if self.frame_count % 30 == 0:
                    self.analyze_frame(frame_rgb)

    def browse_video(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv;*.flv")]
        )
        if file_path:
            self.stop_camera()
            self.current_video_path = file_path
            self.play_video()

    def toggle_video(self):
        if not self.video_active:
            self.browse_video()
        else:
            self.stop_video()
            self.btn_video.configure(text="🎥 Video")

    def play_video(self):
        if hasattr(self, 'placeholder_label') and self.placeholder_label.winfo_exists():
            self.placeholder_label.place_forget()
        if not self.current_video_path:
            return
        
        self.video_active = True
        self.btn_video.configure(text="⏹ Stop Video", fg_color="#ef476f")
        threading.Thread(target=self.video_loop, daemon=True).start()

    def video_loop(self):
        cap = cv2.VideoCapture(self.current_video_path)
        
        if not cap.isOpened():
            self.video_active = False
            self.btn_video.configure(text="🎥 Video")
            return
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = 1.0 / fps if fps > 0 else 0.033
        
        frame_num = 0
        while self.video_active and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img.thumbnail((800, 600))
            
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.display_label.configure(image=photo)
            self.display_label.image = photo
            
            if self.models_loaded and frame_num % 10 == 0:
                self.analyze_frame(frame_rgb)
            
            frame_num += 1
            time.sleep(delay)
        
        cap.release()
        self.video_active = False
        self.btn_video.configure(text="🎥 Video")

    def stop_video(self):
        self.video_active = False

    def analyze_frame(self, frame):
        if not self.species_model or not self.disease_model:
            import random
            species = random.choice(self.species_classes)
            disease = random.choice(self.disease_classes)
            self.species_label.configure(text=species)
            self.disease_label.configure(text=disease,
                                        text_color="#00c853" if "Healthy" in disease else "#ffd60a")
            return
        
        try:
            img = cv2.resize(frame, (224, 224))
            img_array = np.expand_dims(img / 255.0, 0).astype(np.float32)
            
            species_pred = self.species_model.predict(img_array, verbose=0)
            disease_pred = self.disease_model.predict(img_array, verbose=0)
            
            species = self.species_classes[np.argmax(species_pred)]
            disease = self.disease_classes[np.argmax(disease_pred)]
            
            self.species_label.configure(text=species)
            self.disease_label.configure(text=disease,
                                        text_color="#00c853" if "Healthy" in disease else "#ffd60a")
        except:
            pass

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.stop_camera()
            self.stop_video()
            self.current_image = file_path
            self.display_image(file_path)

    def display_image(self, path):
        if hasattr(self, 'placeholder_label') and self.placeholder_label.winfo_exists():
            self.placeholder_label.place_forget()
        img = Image.open(path)
        img.thumbnail((800, 600))
        photo = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        self.display_label.configure(image=photo)
        self.display_label.image = photo

    def quick_analyze(self):
        if hasattr(self, 'current_image') and self.current_image:
            self.analyze_image(self.current_image)

    def analyze_image(self, path):
        if not self.species_model or not self.disease_model:
            import random
            species = random.choice(self.species_classes)
            disease = random.choice(self.disease_classes)
            
            self.species_label.configure(text=species)
            self.disease_label.configure(text=disease,
                                        text_color="#00c853" if "Healthy" in disease else "#ffd60a")
            
            remedy_text = self._build_detailed_info(species, disease, demo_mode=True)
            
            self.remedy_box.configure(state="normal")
            self.remedy_box.delete("0.0", END)
            self.remedy_box.insert("0.0", remedy_text)
            self.remedy_box.configure(state="disabled")
            return
        
        try:
            img = tf.keras.preprocessing.image.load_img(path, target_size=(224, 224))
            img_array = np.expand_dims(tf.keras.preprocessing.image.img_to_array(img) / 255.0, 0)

            species_pred = self.species_model.predict(img_array, verbose=0)
            disease_pred = self.disease_model.predict(img_array, verbose=0)

            species = self.species_classes[np.argmax(species_pred)]
            disease = self.disease_classes[np.argmax(disease_pred)]

            self.species_label.configure(text=species)
            self.disease_label.configure(text=disease,
                                        text_color="#00c853" if "Healthy" in disease else "#ffd60a")

            remedy_text = self._build_detailed_info(species, disease, demo_mode=False)

            self.remedy_box.configure(state="normal")
            self.remedy_box.delete("0.0", END)
            self.remedy_box.insert("0.0", remedy_text)
            self.remedy_box.configure(state="disabled")
        except Exception as e:
            print(f"Analysis error: {e}")

    def _build_detailed_info(self, species, disease, demo_mode=False):
        """Build comprehensive information about detected species and health status"""
        info_text = ""
        
        if demo_mode:
            info_text += "⚠️ DEMO MODE - Simulated Predictions\n"
            info_text += "="*50 + "\n\n"
        
        info_text += f"🐟 SPECIES: {species}\n"
        info_text += "="*50 + "\n"
        
        species_info = get_species_info(species)
        if species_info:
            info_text += f"Scientific Name: {species_info.get('scientific_name', 'N/A')}\n"
            info_text += f"Common Names: {', '.join(species_info.get('common_names', []))}\n\n"
            info_text += f"📝 Description:\n{species_info.get('description', 'N/A')}\n\n"
            info_text += "✨ Key Characteristics:\n"
            for char in species_info.get('characteristics', [])[:5]:
                info_text += f"  • {char}\n"
            info_text += "\n"
            info_text += f"🌊 Habitat: {species_info.get('habitat', 'N/A')}\n"
            info_text += f"🍽️ Diet: {species_info.get('diet', 'N/A')}\n"
            info_text += f"⏳ Lifespan: {species_info.get('lifespan', 'N/A')}\n\n"
            info_text += "🔧 Care Requirements:\n"
            for req in species_info.get('care_requirements', [])[:5]:
                info_text += f"  • {req}\n"
            info_text += "\n"
        else:
            info_text += f"Species information not available in database.\n\n"
        
        info_text += f"🏥 HEALTH STATUS: {disease}\n"
        info_text += "="*50 + "\n"
        
        if disease in DISEASE_INFO:
            disease_data = DISEASE_INFO[disease]
            info_text += f"Type: {disease_data.get('type', 'N/A')}\n\n"
            symptoms = disease_data.get('symptoms', [])
            if symptoms:
                info_text += "⚠️ Symptoms:\n"
                for symptom in symptoms:
                    info_text += f"  • {symptom}\n"
                info_text += "\n"
            remedies = disease_data.get('remedies', [])
            if remedies:
                info_text += "💊 Treatment Protocol:\n"
                for i, remedy in enumerate(remedies, 1):
                    info_text += f"  {i}. {remedy}\n"
                info_text += "\n"
        elif "Healthy" in disease:
            info_text += "✅ Fish appears healthy!\n\n"
            info_text += "Maintenance Recommendations:\n"
            info_text += "  • Continue regular water testing\n"
            info_text += "  • Maintain balanced diet (feed 2-3 times daily)\n"
            info_text += "  • Perform weekly water changes (20-30%)\n"
            info_text += "  • Monitor behavior and appetite daily\n"
            info_text += "  • Keep tank clean and well-filtered\n\n"
        else:
            info_text += f"Detailed treatment information not available.\n"
            info_text += "Consult with aquatic veterinarian for proper diagnosis.\n\n"
        
        if demo_mode:
            info_text += "\n" + "="*50 + "\n"
            info_text += "Note: Train and load models for real predictions.\n"
        
        return info_text

    def send_message(self, event=None):
        msg = self.chat_entry.get().strip()
        if not msg:
            return
        
        self.chat_entry.delete(0, END)
        self.update_chat(f"You: {msg}\n")
        threading.Thread(target=self.get_ai_response, args=(msg,), daemon=True).start()

    def get_ai_response(self, msg):
        response = self.aquabot.chat(msg)
        self.update_chat(f"🤖 AI: {response}\n\n")

    def update_chat(self, text):
        self.chat_history.configure(state="normal")
        self.chat_history.insert(END, text)
        self.chat_history.see(END)
        self.chat_history.configure(state="disabled")

    def on_closing(self):
        self.stop_camera()
        self.stop_video()
        self.destroy()

if __name__ == "__main__":
    app = AquaVisionPro()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
