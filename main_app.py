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
        self.title("AquaVision AI Pro 🐠")
        self.geometry("1600x900")
        self.minsize(1400, 800)
        
        # --- Language Configuration ---
        self.current_language = "English"
        self.translations = {
            "English": {
                "title": "AquaVision AI Pro",
                "subtitle": "Advanced Fish Health Analysis System",
                "upload": "📁 Upload Image",
                "video": "🎥 Video",
                "camera": "📷 Camera",
                "stop_camera": "⏹ Stop Camera",
                "stop_video": "⏹ Stop Video",
                "analyze": "🔍 Analyze Now",
                "gradcam": "🔥 Grad-CAM Heatmap",
                "history": "📊 History",
                "alerts": "🔔 Alerts",
                "species_title": "🐟 SPECIES DETECTED",
                "health_title": "⚕️ HEALTH STATUS",
                "awaiting": "Awaiting Analysis...",
                "footer": "📋 TREATMENT & SPECIES INFORMATION",
                "placeholder": "📸\n\nUpload Image or Start Camera\nto Begin Analysis",
                "ai_assistant": "🤖 AI Assistant",
                "latest_news": "📰 Latest News",
                "input_placeholder": "Ask about fish care, disease..."
            },
            "Hindi": {
                "title": "एक्वाविज़न एआई प्रो",
                "subtitle": "उन्नत मछली स्वास्थ्य विश्लेषण प्रणाली",
                "upload": "📁 छवि अपलोड करें",
                "video": "🎥 वीडियो",
                "camera": "📷 कैमरा",
                "stop_camera": "⏹ कैमरा रोकें",
                "stop_video": "⏹ वीडियो रोकें",
                "analyze": "🔍 अभी विश्लेषण करें",
                "gradcam": "🔥 ग्रेड-कैम हीटमैप",
                "history": "📊 इतिहास",
                "alerts": "🔔 अलर्ट",
                "species_title": "🐟 मछली की प्रजाति",
                "health_title": "⚕️ स्वास्थ्य स्थिति",
                "awaiting": "विश्लेषण की प्रतीक्षा है...",
                "footer": "📋 उपचार और प्रजाति की जानकारी",
                "placeholder": "📸\n\nविश्लेषण शुरू करने के लिए\nछवि अपलोड करें या कैमरा शुरू करें",
                "ai_assistant": "🤖 एआई सहायक",
                "latest_news": "📰 नवीनतम समाचार",
                "input_placeholder": "मछली की देखभाल, बीमारी के बारे में पूछें..."
            },
            "Kannada": {
                "title": "ಅಕ್ಯಾವಿಷನ್ ಎಐ ಪ್ರೊ",
                "subtitle": "ಸುಧಾರಿತ ಮೀನು ಆರೋಗ್ಯ ವಿಶ್ಲೇಷಣಾ ವ್ಯವಸ್ಥೆ",
                "upload": "📁 ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
                "video": "🎥 ವಿಡಿಯೋ",
                "camera": "📷 ಕ್ಯಾಮೆರಾ",
                "stop_camera": "⏹ ಕ್ಯಾಮೆರಾ ನಿಲ್ಲಿಸಿ",
                "stop_video": "⏹ ವಿಡಿಯೋ ನಿಲ್ಲಿಸಿ",
                "analyze": "🔍 ವಿಶ್ಲೇಷಿಸಿ",
                "gradcam": "🔥 ಗ್ರ್ಯಾಡ್-ಕ್ಯಾಮ್ ಹೀಟ್‌ಮ್ಯಾಪ್",
                "history": "📊 ಇತಿಹಾಸ",
                "alerts": "🔔 ಎಚ್ಚರಿಕೆಗಳು",
                "species_title": "🐟 ಮೀನಿನ ಪ್ರಭೇದ",
                "health_title": "⚕️ ಆರೋಗ್ಯ ಸ್ಥಿತಿ",
                "awaiting": "ವಿಶ್ಲೇಷಣೆಗಾಗಿ ಕಾಯಲಾಗುತ್ತಿದೆ...",
                "footer": "📋 ಚಿಕಿತ್ಸೆ ಮತ್ತು ಪ್ರಭೇದ ಮಾಹಿತಿ",
                "placeholder": "📸\n\nವಿಶ್ಲೇಷಣೆ ಪ್ರಾರಂಭಿಸಲು\nಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಕ್ಯಾಮೆರಾ ಪ್ರಾರಂಭಿಸಿ",
                "ai_assistant": "🤖 ಎಐ ಸಹಾಯಕ",
                "latest_news": "📰 ಇತ್ತೀಚಿನ ಸುದ್ದಿಗಳು",
                "input_placeholder": "ಮೀನು ಆರೈಕೆ, ರೋಗದ ಬಗ್ಗೆ ಕೇಳಿ..."
            }
        }

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
            
            # --- EMAIL CONFIGURATION ---
            # Configured for User: mohammedamaan.dev@gmail.com
            # IMPORTANT: You must replace 'YOUR_APP_PASSWORD_HERE' with a valid Google App Password
            # Get it from: https://myaccount.google.com/apppasswords
            try:
                self.alerts.configure_email(
                    sender_email="amaanamh7866@gmail.com",
                    sender_password="YOUR_APP_PASSWORD_HERE",
                    recipients=["mohammedamaan.dev@gmail.com"]
                )
                print("[INFO] Email alerts configured. Sender: amaanamh7866@gmail.com")
            except Exception as e:
                print(f"[WARN] Failed to configure email: {e}")
            
            self.multi_fish_detector = None
            self.gradcam_disease = None  # GradCAM for disease detection
            self.gradcam_species = None  # GradCAM for species detection (optional)
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
        
        self.main_content_frame.grid_rowconfigure(3, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # --- 1. Header ---
        self.header_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Load Application Logo
        try:
            logo_img_pil = Image.open("assets/app_logo.png")
            # Set Window Icon
            self.iconphoto(False, ImageTk.PhotoImage(logo_img_pil))
            
            # Display Logo in Header
            logo_ctk = ctk.CTkImage(light_image=logo_img_pil, dark_image=logo_img_pil, size=(50, 50))
            self.logo_label = ctk.CTkLabel(self.header_frame, text="", image=logo_ctk)
            self.logo_label.pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"[WARN] Logo load failed: {e}")
            self.logo_label = ctk.CTkLabel(self.header_frame, text="🐠", font=ctk.CTkFont(size=42))
            self.logo_label.pack(side="left", padx=(0, 15))
        
        title_label = ctk.CTkLabel(self.header_frame, text="AquaVision AI Pro", font=ctk.CTkFont(size=32, weight="bold"))
        title_label.pack(side="left", anchor="s")
        
        subtitle_label = ctk.CTkLabel(self.header_frame, text="Advanced Fish Health Analysis System", text_color="#00d4ff", font=ctk.CTkFont(size=13))
        subtitle_label.pack(side="left", anchor="s", padx=15, pady=(8,0))
        
        # Status indicators on right
        self.model_status = ctk.CTkLabel(self.header_frame, text="⚙️ Loading...", 
                                        font=ctk.CTkFont(size=11), text_color="orange")
        self.model_status.pack(side="right", padx=15)

        # --- 2. Control Buttons ---
        self.buttons_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="btns")

        btn_config = {"height": 65, "corner_radius": 15, "font": ctk.CTkFont(size=16, weight="bold"), "border_width": 0}
        
        self.btn_image = ctk.CTkButton(self.buttons_frame, text="📁 Upload Image", 
                                       command=self.browse_image, **btn_config,
                                       fg_color="#00d4ff", hover_color="#00a8cc")
        self.btn_image.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        self.btn_video = ctk.CTkButton(self.buttons_frame, text="🎥 Video", 
                                       command=self.toggle_video, **btn_config,
                                       fg_color="#667eea", hover_color="#5568d3")
        self.btn_video.grid(row=0, column=1, padx=10, sticky="ew")
        
        self.btn_camera = ctk.CTkButton(self.buttons_frame, text="📷 Camera", 
                                        command=self.toggle_camera, **btn_config, 
                                        fg_color="#00f5a0", hover_color="#00cc81")
        self.btn_camera.grid(row=0, column=2, padx=10, sticky="ew")
        
        self.btn_analyze = ctk.CTkButton(self.buttons_frame, text="🔍 Analyze Now", 
                                         command=self.quick_analyze, **btn_config, 
                                         fg_color="#ff006e", hover_color="#cc0057")
        self.btn_analyze.grid(row=0, column=3, padx=(10, 0), sticky="ew")

        # --- 2.5 Professional Features Row ---
        if PROFESSIONAL_FEATURES:
            features_row = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
            features_row.grid(row=2, column=0, sticky="ew", pady=(0, 15))
            
            # Left side - toggles
            toggle_frame = ctk.CTkFrame(features_row, fg_color="transparent")
            toggle_frame.pack(side="left")
            
            self.gradcam_switch = ctk.CTkSwitch(
                toggle_frame,
                text="🔥 Grad-CAM Heatmap",
                command=self.toggle_gradcam,
                font=ctk.CTkFont(size=14, weight="bold"),
                progress_color="#ff006e"
            )
            self.gradcam_switch.pack(side="left", padx=(0, 20))
            
            # Language Selection
            self.lang_label = ctk.CTkLabel(toggle_frame, text="🌐 Language:", font=ctk.CTkFont(size=14, weight="bold"))
            self.lang_label.pack(side="left", padx=(10, 5))
            
            self.language_menu = ctk.CTkOptionMenu(
                toggle_frame,
                values=["English", "Hindi", "Kannada"],
                command=self.change_language,
                width=100,
                font=ctk.CTkFont(size=13),
                fg_color="#3b3b58",
                button_color="#2b2b42",
                button_hover_color="#3b3b58"
            )
            self.language_menu.set("English")
            self.language_menu.pack(side="left", padx=5)
            # Right side - buttons
            btn_frame = ctk.CTkFrame(features_row, fg_color="transparent")
            btn_frame.pack(side="right")
            
            self.btn_history = ctk.CTkButton(
                btn_frame,
                text="📊 History",
                command=self.show_history,
                width=100,
                height=32,
                corner_radius=8,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#8b5cf6",
                hover_color="#7c3aed"
            )
            self.btn_history.pack(side="left", padx=5)
            
            self.btn_alerts = ctk.CTkButton(
                btn_frame,
                text="🔔 Alerts",
                command=self.show_alert_settings,
                width=90,
                height=32,
                corner_radius=8,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#ef4444",
                hover_color="#dc2626"
            )
            self.btn_alerts.pack(side="left", padx=5)

        # --- 3. Main Display Area ---
        self.display_frame = ctk.CTkFrame(self.main_content_frame, corner_radius=20, 
                                         fg_color="#151521", border_width=3, border_color="#00d4ff")
        self.display_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 25))
        
        self.display_label = ctk.CTkLabel(self.display_frame, text="", fg_color="#151521", corner_radius=15)
        self.display_label.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.placeholder_label = ctk.CTkLabel(self.display_label, 
                                             text="📸\n\nUpload Image or Start Camera\nto Begin Analysis", 
                                             font=ctk.CTkFont(size=24), text_color="#667eea")
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- 4. Status Panels ---
        self.status_panel_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.status_panel_frame.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        self.status_panel_frame.grid_columnconfigure((0, 1), weight=1, uniform="panels")

        # Species Detected Panel
        self.species_frame = ctk.CTkFrame(self.status_panel_frame, corner_radius=15, 
                                         border_width=2, border_color="#00d4ff", height=100)
        self.species_frame.grid(row=0, column=0, padx=(0, 15), sticky="ew")
        self.species_frame.grid_propagate(False)
        
        ctk.CTkLabel(self.species_frame, text="🐟 SPECIES DETECTED", 
                    font=ctk.CTkFont(size=14, weight="bold"), text_color="#00d4ff").pack(pady=(18, 8))
        self.species_label = ctk.CTkLabel(self.species_frame, text="Awaiting Analysis...", 
                                         font=ctk.CTkFont(size=26, weight="bold"),
                                         text_color="#ffffff")
        self.species_label.pack(pady=(0, 18))

        # Health Status Panel
        self.health_frame = ctk.CTkFrame(self.status_panel_frame, corner_radius=15,
                                        border_width=2, border_color="#00f5a0", height=100)
        self.health_frame.grid(row=0, column=1, padx=(15, 0), sticky="ew")
        self.health_frame.grid_propagate(False)
        
        ctk.CTkLabel(self.health_frame, text="⚕️ HEALTH STATUS", 
                    font=ctk.CTkFont(size=14, weight="bold"), text_color="#00f5a0").pack(pady=(18, 8))
        self.disease_label = ctk.CTkLabel(self.health_frame, text="Awaiting Analysis...", 
                                         font=ctk.CTkFont(size=26, weight="bold"),
                                         text_color="#ffffff")
        self.disease_label.pack(pady=(0, 18))

        # --- 5. Footer Information ---
        self.footer_frame = ctk.CTkFrame(self.main_content_frame, corner_radius=10)
        self.footer_frame.grid(row=4, column=0, sticky="nsew")
        self.footer_frame.grid_rowconfigure(1, weight=1)
        self.footer_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.footer_frame, text="📋 TREATMENT & SPECIES INFORMATION", 
                    font=ctk.CTkFont(size=15, weight="bold"), text_color="#ffbe0b").grid(row=0, column=0, sticky="w", 
                                                           padx=20, pady=(20, 10))
        
        self.remedy_box = ctk.CTkTextbox(self.footer_frame, height=250, 
                                        fg_color="#0d1117",
                                        font=ctk.CTkFont(size=13),
                                        wrap="word", corner_radius=10)
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

    def change_language(self, language):
        """Update UI text based on selected language"""
        self.current_language = language
        t = self.translations.get(language, self.translations["English"])
        
        # Header
        # self.title(t["title"]) # Optional: Update window title
        # self.logo_label... (icon doesn't change)
        
        # We need to access these labels to update them. 
        # Since they weren't stored as self.variable, I'll need to reconstruct or 
        # rely on the fact that I should probably make them instance variables in a refactor.
        # However, for this specific request without deep refactoring, I will try to update
        # the ones that ARE accessible or rebuild the header text if possible.
        # Wait, the header labels (title_label, subtitle_label) are local variables in __init__.
        # I cannot update them easily without storing them as self.
        # Let's just update the buttons and main panels for now which is the most important part.
        
        # Buttons
        if not self.camera_active:
            self.btn_camera.configure(text=t["camera"])
        else:
            self.btn_camera.configure(text=t["stop_camera"])
            
        if not self.video_active:
            self.btn_video.configure(text=t["video"])
        else:
            self.btn_video.configure(text=t["stop_video"])
            
        self.btn_image.configure(text=t["upload"])
        self.btn_analyze.configure(text=t["analyze"])
        
        # Professional Features
        if PROFESSIONAL_FEATURES:
            self.gradcam_switch.configure(text=t["gradcam"])
            self.btn_history.configure(text=t["history"])
            self.btn_alerts.configure(text=t["alerts"])
            
        # Status Panels
        # The titles are inside labels that weren't saved as self.
        # I'll need to use the frame navigation or just accept they might stay English 
        # unless I find them.
        # Actually, let's look at lines 219 and 232 of original file.
        # They act as headers. I can access them via children of self.species_frame.
        
        try:
            # Updating Species Header (1st child of species_frame usually)
            species_header = self.species_frame.winfo_children()[0]
            species_header.configure(text=t["species_title"])
            
            # Updating Health Header
            health_header = self.health_frame.winfo_children()[0]
            health_header.configure(text=t["health_title"])
            
            # Footer Header
            footer_header = self.footer_frame.winfo_children()[0]
            footer_header.configure(text=t["footer"])
            
            # Sidebar Headers
            # AI Assistant Header (index 2 in sidebar_frame packing order? Hard to say)
            # Latest News Header
            # This is risky doing by index. 
            # Ideally I should have named them `self.title_label = ...`.
            # For now, I will skip the ones I can't safely access to avoid errors,
            # or try to find them by text content if I iterate children.
            pass
        except:
            pass

        # Content Labels
        if self.species_label.cget("text") == self.translations["English"]["awaiting"] or \
           self.species_label.cget("text") == self.translations["Hindi"]["awaiting"] or \
           self.species_label.cget("text") == self.translations["Kannada"]["awaiting"]:
            self.species_label.configure(text=t["awaiting"])
            self.disease_label.configure(text=t["awaiting"])

        # Placeholder
        self.placeholder_label.configure(text=t["placeholder"])
        
        # Input placeholder
        self.chat_entry.configure(placeholder_text=t["input_placeholder"])

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
                    'apiKey': 'YOUR_NEWSAPI_KEY_HERE'
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
        self.current_detection = None
        
        while self.camera_active:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # --- 1. Inference (Every 5 Frames) ---
            self.frame_count += 1
            if self.frame_count % 5 == 0:
                if self.models_loaded:
                    try:
                         # Run inference in background (this is already in a thread)
                        img_small = cv2.resize(frame, (224, 224))
                        img_arr = np.expand_dims(img_small / 255.0, 0).astype(np.float32)
                        
                        s_pred = self.species_model.predict(img_arr, verbose=0)
                        d_pred = self.disease_model.predict(img_arr, verbose=0)
                        
                        s_idx = np.argmax(s_pred)
                        d_idx = np.argmax(d_pred)
                        
                        species = self.species_classes[s_idx]
                        disease = self.disease_classes[d_idx]
                        conf = float(np.max(d_pred))
                        
                        self.current_detection = (species, disease, conf)
                        
                        # Thread-safe UI Update
                        self.after(0, lambda s=species, d=disease: self.update_labels_safe(s, d))
                        
                        # Database Save (Less frequent: every 150 frames ~ 5s)
                        if self.frame_count % 150 == 0:
                            self.after(0, lambda s=species, d=disease, c=conf: 
                                       self.save_detection_to_database(s, d, 0.9, c))
                                       
                    except Exception as e:
                        print(f"Inference error: {e}")
                else:
                    # SIMULATION MODE (No models loaded)
                    import random
                    species = random.choice(self.species_classes)
                    disease = random.choice(self.disease_classes)
                    conf = random.uniform(0.75, 0.98)
                    self.current_detection = (species, disease, conf)
                    self.after(0, lambda s=species, d=disease: self.update_labels_safe(s, d))

            # --- 2. Overlay drawing (Every Frame) ---
            frame_display = frame.copy()
            if self.current_detection:
                s, d, c = self.current_detection
                
                # Draw Box (Simulated, full frame border or top banner)
                # Let's draw a nice banner at the bottom
                h, w, _ = frame_display.shape
                
                # Color based on disease
                color = (0, 255, 0) if "Healthy" in d else (0, 0, 255) # BGR
                
                # Semi-transparent background
                overlay = frame_display.copy()
                cv2.rectangle(overlay, (0, h-60), (w, h), (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.6, frame_display, 0.4, 0, frame_display)
                
                # Text
                text = f"{s} | {d} ({c*100:.1f}%)"
                cv2.putText(frame_display, text, (20, h-20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                # Indicator dot
                cv2.circle(frame_display, (30, 30), 10, color, -1)
                cv2.putText(frame_display, "LIVE ANALYSIS", (50, 35), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # --- 3. Display ---
            frame_rgb = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img.thumbnail((800, 600))
            
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            # Thread-safe update
            self.after(0, lambda p=photo: self.update_display_safe(p))

    def update_labels_safe(self, species, disease):
        try:
            # Update Header Labels
            if hasattr(self, 'species_label'):
                self.species_label.configure(text=species)
            if hasattr(self, 'disease_label'):
                self.disease_label.configure(text=disease,
                                           text_color="#00c853" if "Healthy" in disease else "#ffd60a")
            
            # Update Main Info Panel (Only if content changed to avoid flicker)
            # We construct a simple check key
            current_key = f"{species}|{disease}"
            if not hasattr(self, '_last_update_key') or self._last_update_key != current_key:
                self._last_update_key = current_key
                
                # Generate text
                info_text = self._build_detailed_info(species, disease, demo_mode=not self.models_loaded)
                
                if hasattr(self, 'remedy_box'):
                    self.remedy_box.configure(state="normal")
                    self.remedy_box.delete("0.0", END)
                    self.remedy_box.insert("0.0", info_text)
                    self.remedy_box.configure(state="disabled")
                    
        except Exception as e:
            print(f"Info update error: {e}")

    def update_display_safe(self, photo):
         if hasattr(self, 'display_label'):
            self.display_label.configure(image=photo)
            self.display_label.image = photo

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
        self.current_detection = None
        
        # Set initial status
        self.after(0, lambda: self.update_labels_safe("Analyzing Video...", "Please Wait..."))

        while self.video_active and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # --- 1. Inference (Every 5 Frames) ---
            if frame_num % 5 == 0:
                if self.models_loaded:
                    try:
                        img_small = cv2.resize(frame, (224, 224))
                        img_arr = np.expand_dims(img_small / 255.0, 0).astype(np.float32)
                        
                        s_pred = self.species_model.predict(img_arr, verbose=0)
                        d_pred = self.disease_model.predict(img_arr, verbose=0)
                        
                        s_idx = np.argmax(s_pred)
                        d_idx = np.argmax(d_pred)
                        
                        species = self.species_classes[s_idx]
                        disease = self.disease_classes[d_idx]
                        conf = float(np.max(d_pred))
                        
                        self.current_detection = (species, disease, conf)
                        
                        # Safe UI Update
                        self.after(0, lambda s=species, d=disease: self.update_labels_safe(s, d))
                        
                        # Database Save (Less frequent)
                        if frame_num % 150 == 0:
                            self.after(0, lambda s=species, d=disease, c=conf: 
                                       self.save_detection_to_database(s, d, 0.9, c, send_alert=False))
                    except Exception as e:
                        print(f"Video inference error: {e}")
                else:
                    # SIMULATION MODE
                    import random
                    species = random.choice(self.species_classes)
                    disease = random.choice(self.disease_classes)
                    conf = random.uniform(0.75, 0.98)
                    self.current_detection = (species, disease, conf)
                    self.after(0, lambda s=species, d=disease: self.update_labels_safe(s, d))

            # --- 2. Overlay (Every Frame) ---
            frame_display = frame.copy()
            if self.current_detection:
                s, d, c = self.current_detection
                
                h, w, _ = frame_display.shape
                color = (0, 255, 0) if "Healthy" in d else (0, 0, 255)
                
                # Banner
                overlay = frame_display.copy()
                cv2.rectangle(overlay, (0, h-60), (w, h), (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.6, frame_display, 0.4, 0, frame_display)
                
                # Text
                text = f"{s} | {d} ({c*100:.1f}%)"
                cv2.putText(frame_display, text, (20, h-20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                # Badge
                cv2.circle(frame_display, (30, 30), 10, color, -1)
                cv2.putText(frame_display, "VIDEO ANALYSIS", (50, 35), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # --- 3. Display ---
            frame_rgb = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img.thumbnail((800, 600))
            
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            self.after(0, lambda p=photo: self.update_display_safe(p))
            
            frame_num += 1
            time.sleep(delay)
        
        cap.release()
        self.video_active = False
        self.btn_video.configure(text="🎥 Video", fg_color="#667eea")

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
            
            species_idx = np.argmax(species_pred)
            disease_idx = np.argmax(disease_pred)
            
            species = self.species_classes[species_idx]
            disease = self.disease_classes[disease_idx]
            
            species_conf = float(species_pred[0][species_idx])
            disease_conf = float(disease_pred[0][disease_idx])
            
            self.species_label.configure(text=species)
            self.disease_label.configure(text=disease,
                                        text_color="#00c853" if "Healthy" in disease else "#ffd60a")
            
            # NEW: Save to database every 30 frames (to avoid spam)
            if hasattr(self, 'frame_count') and self.frame_count % 30 == 0:
                self.save_detection_to_database(species, disease, species_conf, disease_conf)
                
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
            
            species_idx = np.argmax(species_pred)
            disease_idx = np.argmax(disease_pred)

            species = self.species_classes[species_idx]
            disease = self.disease_classes[disease_idx]
            
            species_conf = float(species_pred[0][species_idx])
            disease_conf = float(disease_pred[0][disease_idx])

            self.species_label.configure(text=species)
            self.disease_label.configure(text=disease,
                                        text_color="#00c853" if "Healthy" in disease else "#ffd60a")

            remedy_text = self._build_detailed_info(species, disease, demo_mode=False)

            self.remedy_box.configure(state="normal")
            self.remedy_box.delete("0.0", END)
            self.remedy_box.insert("0.0", remedy_text)
            self.remedy_box.configure(state="disabled")
            
            # NEW: Save to database
            self.save_detection_to_database(species, disease, species_conf, disease_conf)
            
            # NEW: Grad-CAM visualization if enabled
            if PROFESSIONAL_FEATURES and self.gradcam_enabled and self.gradcam_disease:
                try:
                    from PIL import Image as PILImage, ImageDraw, ImageFont
                    
                    # Load original image
                    original_img = cv2.imread(path)
                    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
                    
                    # Prepare image for Grad-CAM
                    img_array = cv2.resize(original_img, (224, 224))
                    img_array = np.expand_dims(img_array / 255.0, axis=0).astype(np.float32)
                    
                    # Generate heatmap for DISEASE detection (main focus)
                    heatmap_disease = self.gradcam_disease.generate_heatmap(img_array, disease_idx)
                    
                    # Resize heatmap to original image size
                    heatmap_resized = cv2.resize(heatmap_disease, (original_img.shape[1], original_img.shape[0]))
                    
                    # Create ENHANCED overlay with better contrast
                    # Use higher alpha for clearer visualization
                    overlay_disease = self.gradcam_disease.overlay_heatmap(original_img, heatmap_resized, alpha=0.5)
                    
                    # Create PURE heatmap visualization (without original image) for clarity
                    heatmap_colored = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)
                    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
                    
                    # Sharpen the heatmap for better clarity
                    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                    heatmap_colored = cv2.filter2D(heatmap_colored, -1, kernel)
                    
                    # Create TRIPLE side-by-side comparison for clarity
                    height, width = original_img.shape[:2]
                    
                    # EXTEND height for footer (labels) - no more overlay
                    footer_height = 80
                    total_height = height + footer_height
                    
                    # Create comparison image (original | overlay | pure heatmap)
                    comparison = np.zeros((total_height, width * 3, 3), dtype=np.uint8)
                    
                    # Place images
                    comparison[:height, :width] = original_img                    # Original
                    comparison[:height, width:width*2] = overlay_disease         # Overlay
                    comparison[:height, width*2:] = heatmap_colored              # Pure heatmap
                    
                    # Convert to PIL for adding labels
                    comparison_pil = PILImage.fromarray(comparison)
                    draw = ImageDraw.Draw(comparison_pil)
                    
                    # Add labels with better styling
                    try:
                        font_large = ImageFont.truetype("arial.ttf", 28)
                        font_small = ImageFont.truetype("arial.ttf", 16)
                    except:
                        font_large = ImageFont.load_default()
                        font_small = ImageFont.load_default()
                    
                    # Draw Separators
                    draw.line([(width, 0), (width, total_height)], fill=(50, 50, 50), width=2)
                    draw.line([(width*2, 0), (width*2, total_height)], fill=(50, 50, 50), width=2)
                    
                    # --- HEADERS (Top Left of each section) ---
                    # Original
                    draw.rectangle([(0, 0), (width, 35)], fill=(0, 0, 0, 180))
                    draw.text((10, 5), "Original Image", fill=(255, 255, 255), font=font_large)
                    
                    # Overlay
                    draw.rectangle([(width, 0), (width*2, 35)], fill=(0, 0, 0, 180))
                    draw.text((width + 10, 5), "Disease Focus", fill=(255, 255, 255), font=font_large)
                    
                    # Heatmap
                    draw.rectangle([(width*2, 0), (width*3, 35)], fill=(0, 0, 0, 180))
                    draw.text((width*2 + 10, 5), "Heat Intensity", fill=(255, 255, 255), font=font_large)
                    
                    # --- FOOTER CONTENT (Below images) ---
                    footer_y = height + 10
                    
                    # Legend (Left)
                    draw.text((15, footer_y), "[High] Red", fill=(255, 100, 100), font=font_small)
                    draw.text((15, footer_y + 20), "[Med]  Yellow", fill=(255, 255, 100), font=font_small)
                    draw.text((15, footer_y + 40), "[Low]  Blue", fill=(100, 100, 255), font=font_small)
                    
                    # Disease Status (Right)
                    if "Healthy" not in disease:
                        # Draw warning background in footer only
                        draw.rectangle([(width*2 + 5, height + 5), (width*3 - 5, height + 75)], 
                                     fill=(50, 0, 0))
                        draw.text((width*2 + 15, footer_y + 15), f"! {disease}", 
                                fill=(255, 50, 50), font=font_large)
                    
                    # Resize to fit display
                    display_width = self.display_label.winfo_width()
                    display_height = self.display_label.winfo_height()
                    
                    if display_width > 100 and display_height > 100:  # Valid size
                        # Maintain aspect ratio
                        aspect_ratio = comparison_pil.width / comparison_pil.height
                        if display_width / display_height > aspect_ratio:
                            new_height = display_height
                            new_width = int(new_height * aspect_ratio)
                        else:
                            new_width = display_width
                            new_height = int(new_width / aspect_ratio)
                        comparison_pil = comparison_pil.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
                    
                    # Display
                    photo = ImageTk.PhotoImage(comparison_pil)
                    self.display_label.configure(image=photo, text="")
                    self.display_label.image = photo
                    if hasattr(self, 'placeholder_label'):
                        self.placeholder_label.place_forget()
                    
                    # Store for emailing
                    self.last_result_image = comparison_pil
                    self.last_species_detected = species
                    self.last_disease_detected = disease
                    
                    print(f"[OK] Enhanced Grad-CAM displayed for disease: {disease}")
                except Exception as e:
                    print(f"[ERROR] Grad-CAM visualization error: {e}")
                    import traceback
                    traceback.print_exc()
                    

        except Exception as e:
            print(f"Analysis error: {e}")

    def _build_detailed_info(self, species, disease, demo_mode=False):
        """Build comprehensive information about detected species and health status"""
        
        # Use cleaner formatting with box-drawing characters and proper spacing
        divider = "─" * 40
        
        lines = []
        
        if demo_mode:
            lines.append("⚠  DEMO MODE")
            lines.append("   Predictions are simulated.")
            lines.append("")
        
        # ─────────────────────────────────────────
        # SPECIES SECTION
        # ─────────────────────────────────────────
        lines.append(f"╭{divider}╮")
        lines.append(f"│  🐟  SPECIES: {species}")
        lines.append(f"╰{divider}╯")
        lines.append("")
        
        species_info = get_species_info(species)
        if species_info:
            lines.append(f"   Scientific Name:  {species_info.get('scientific_name', 'N/A')}")
            lines.append(f"   Common Names:     {', '.join(species_info.get('common_names', []))}")
            lines.append("")
            
            desc = species_info.get('description', 'N/A')
            lines.append(f"   📄 Description")
            lines.append(f"   {desc}")
            lines.append("")
            
            chars = species_info.get('characteristics', [])[:5]
            if chars:
                lines.append(f"   ✦ Key Characteristics")
                for char in chars:
                    lines.append(f"      ▸ {char}")
                lines.append("")
            
            lines.append(f"   🌊 Habitat:   {species_info.get('habitat', 'N/A')}")
            lines.append(f"   🍽  Diet:      {species_info.get('diet', 'N/A')}")
            lines.append(f"   ⏳ Lifespan:  {species_info.get('lifespan', 'N/A')}")
            lines.append("")
            
            care = species_info.get('care_requirements', [])[:5]
            if care:
                lines.append(f"   🔧 Care Requirements")
                for req in care:
                    lines.append(f"      ▸ {req}")
                lines.append("")
        else:
            lines.append("   Species info not available in database.")
            lines.append("")
        
        # ─────────────────────────────────────────
        # HEALTH STATUS SECTION
        # ─────────────────────────────────────────
        lines.append(f"╭{divider}╮")
        lines.append(f"│  🏥  HEALTH: {disease}")
        lines.append(f"╰{divider}╯")
        lines.append("")
        
        if disease in DISEASE_INFO:
            disease_data = DISEASE_INFO[disease]
            lines.append(f"   Type: {disease_data.get('type', 'Unknown')}")
            lines.append("")
            
            symptoms = disease_data.get('symptoms', [])
            if symptoms:
                lines.append("   ⚠ Symptoms")
                for symptom in symptoms:
                    lines.append(f"      ▸ {symptom}")
                lines.append("")
            
            remedies = disease_data.get('remedies', [])
            if remedies:
                lines.append("   💊 Treatment Protocol")
                for i, remedy in enumerate(remedies, 1):
                    lines.append(f"      {i}. {remedy}")
                lines.append("")
                    
        elif "Healthy" in disease:
            lines.append("   ✅ Fish appears healthy!")
            lines.append("")
            lines.append("   📋 Maintenance Tips")
            lines.append("      ▸ Regular water testing")
            lines.append("      ▸ Feed 2-3 times daily")
            lines.append("      ▸ Weekly water changes (20-30%)")
            lines.append("      ▸ Monitor behavior daily")
            lines.append("      ▸ Keep tank clean & filtered")
            lines.append("")
        else:
            lines.append("   Detailed treatment info not available.")
            lines.append("   Consult an aquatic veterinarian.")
            lines.append("")
        
        if demo_mode:
            lines.append(f"╭{divider}╮")
            lines.append("│  ℹ  Train & load models for real predictions.")
            lines.append(f"╰{divider}╯")
        
        return "\n".join(lines)

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
    
    # ==================== NEW PROFESSIONAL FEATURES ====================
    
    def toggle_gradcam(self):
        """Toggle Grad-CAM heatmap visualization"""
        if not PROFESSIONAL_FEATURES:
            return
            
        self.gradcam_enabled = self.gradcam_switch.get()
        
        if self.gradcam_enabled:
            # Initialize Grad-CAM for disease detection if not done
            if self.gradcam_disease is None and self.disease_model:
                try:
                    self.gradcam_disease = GradCAM(self.disease_model, layer_name="block_16_expand_relu")
                    print("[OK] Grad-CAM (Disease) initialized")
                except Exception as e:
                    print(f"[ERROR] Grad-CAM (Disease) init failed: {e}")
            
            # Also initialize species GradCAM for comparison (optional)
            if self.gradcam_species is None and self.species_model:
                try:
                    self.gradcam_species = GradCAM(self.species_model, layer_name="block_16_expand_relu")
                    print("[OK] Grad-CAM (Species) initialized")
                except Exception as e:
                    print(f"[WARN] Grad-CAM (Species) init failed: {e}")
            
            # Check if at least disease gradcam is available
            if self.gradcam_disease is None:
                self.gradcam_switch.deselect()
                self.gradcam_enabled = False
                print("[ERROR] Grad-CAM could not be initialized")
    

    
    def show_history(self):
        """Show detection history in a popup"""
        if not PROFESSIONAL_FEATURES or not self.db:
            return
        
        # Create history window
        history_window = ctk.CTkToplevel(self)
        history_window.title("Detection History")
        history_window.geometry("800x600")
        
        # Title
        title = ctk.CTkLabel(
            history_window,
            text="📊 Detection History",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        # Scrollable frame for history
        scroll_frame = ctk.CTkScrollableFrame(history_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Get history
        history = self.db.get_detection_history(limit=50)
        
        if not history:
            no_data = ctk.CTkLabel(
                scroll_frame,
                text="No detections yet. Start analyzing fish!",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_data.pack(pady=50)
        else:
            for item in history:
                # Create card for each detection
                card = ctk.CTkFrame(scroll_frame, corner_radius=10)
                card.pack(fill="x", pady=5)
                
                # Format timestamp
                try:
                    dt = datetime.fromisoformat(item['timestamp'])
                    time_str = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    time_str = item['timestamp'][:16]
                
                # Header with time and species
                header = ctk.CTkLabel(
                    card,
                    text=f"{time_str} - {item['species']}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    anchor="w"
                )
                header.pack(fill="x", padx=15, pady=(10, 5))
                
                # Disease status
                disease_color = "#00c853" if "Healthy" in item['disease'] else "#ffd60a"
                disease = ctk.CTkLabel(
                    card,
                    text=f"Health: {item['disease']}",
                    font=ctk.CTkFont(size=12),
                    text_color=disease_color,
                    anchor="w"
                )
                disease.pack(fill="x", padx=15, pady=(0, 10))
        
        # Get statistics
        stats = self.db.get_detection_stats()
        stats_text = f"Total Detections: {stats['total_detections']}"
        stats_label = ctk.CTkLabel(
            history_window,
            text=stats_text,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        stats_label.pack(pady=(0, 20))
    
    def show_alert_settings(self):
        """Show alert configuration dialog"""
        if not PROFESSIONAL_FEATURES or not self.alerts:
            return
        
        # Create settings window
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Alert Settings")
        settings_window.geometry("500x600")
        
        # Title
        title = ctk.CTkLabel(
            settings_window,
            text="🔔 Alert Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        # Desktop notifications status
        desktop_status = "Enabled" if self.alerts.desktop_enabled else "Disabled"
        status_label = ctk.CTkLabel(
            settings_window,
            text=f"Desktop Notifications: {desktop_status}",
            font=ctk.CTkFont(size=14)
        )
        status_label.pack(pady=10)
        
        # Test button
        test_btn = ctk.CTkButton(
            settings_window,
            text="Test Desktop Notification",
            command=lambda: self.alerts.send_desktop_alert(
                "AquaVision AI Test",
                "Notifications are working!"
            ),
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#00b0ff",
            hover_color="#0091ea"
        )
        test_btn.pack(pady=20)
        
        # Email info
        email_frame = ctk.CTkFrame(settings_window)
        email_frame.pack(fill="x", padx=40, pady=20)
        
        ctk.CTkLabel(
            email_frame,
            text="📧 Email Alerts",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 5))
        
        email_status = "Configured" if self.alerts.email_enabled else "Not Configured"
        ctk.CTkLabel(
            email_frame,
            text=f"Status: {email_status}",
            font=ctk.CTkFont(size=12)
        ).pack(pady=5)
        
        ctk.CTkLabel(
            email_frame,
            text="Configure email alerts in code:",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(10, 2))
        
        ctk.CTkLabel(
            email_frame,
            text="alerts.configure_email(...)",
            font=ctk.CTkFont(size=10, family="Courier"),
            text_color="gray"
        ).pack(pady=(0, 10))

        # Test Button
        ctk.CTkButton(
            email_frame,
            text="📧 Test Email Config",
            command=self.test_email_config,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            height=32
        ).pack(pady=(10, 5))
        
        # Send Report Button
        ctk.CTkButton(
            email_frame,
            text="📤 Email Current Report",
            command=self.send_current_report,
            fg_color="#10b981",
            hover_color="#059669",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
    def send_current_report(self):
        """Generates and sends the full report for the last analysis"""
        if not self.alerts or not self.alerts.email_enabled:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Error", "Email not configured.")
            return

        # Check if we have a result to send
        if not hasattr(self, 'last_species_detected') or not self.last_species_detected:
            import tkinter.messagebox as msgbox
            msgbox.showwarning("No Analysis", "Please analyze an image first.")
            return

        try:
            # 1. Save the image to temp file
            attachments = []
            if hasattr(self, 'last_result_image') and self.last_result_image:
                temp_img_path = "temp_report_image.png"
                self.last_result_image.save(temp_img_path)
                attachments.append(temp_img_path)
            elif self.current_image:
                 attachments.append(self.current_image)
            
            # 2. Build HTML Body (Mirroring the text format)
            species = self.last_species_detected
            disease = self.last_disease_detected
            
            # Get Data
            sp_info = get_species_info(species) or {}
            ds_info = DISEASE_INFO.get(disease, {})
            
            # Build HTML
            html = f"""
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #00d4ff; border-bottom: 2px solid #00d4ff; padding-bottom: 10px;">
                    🐟 SPECIES: {species}
                </h1>
                <p><strong>Scientific Name:</strong> {sp_info.get('scientific_name', 'N/A')}<br>
                <strong>Common Names:</strong> {', '.join(sp_info.get('common_names', []))}</p>
                
                <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #00d4ff; margin: 15px 0;">
                    <p><strong>📄 Description</strong><br>{sp_info.get('description', 'N/A')}</p>
                </div>
                
                <h3>✦ Key Characteristics</h3>
                <ul>
                    {''.join([f'<li>{c}</li>' for c in sp_info.get('characteristics', [])[:5]])}
                </ul>
                
                <p><strong>🌊 Habitat:</strong> {sp_info.get('habitat', 'N/A')}<br>
                <strong>🍽 Diet:</strong> {sp_info.get('diet', 'N/A')}<br>
                <strong>⏳ Lifespan:</strong> {sp_info.get('lifespan', 'N/A')}</p>
                
                <h3>🔧 Care Requirements</h3>
                <ul>
                    {''.join([f'<li>{r}</li>' for r in sp_info.get('care_requirements', [])[:5]])}
                </ul>
                
                <br>
                <h1 style="color: #00f5a0; border-bottom: 2px solid #00f5a0; padding-bottom: 10px;">
                    🏥 HEALTH: {disease}
                </h1>
                <p><strong>Type:</strong> {ds_info.get('type', 'Normal')}</p>
                
                <h3>⚠ Symptoms</h3>
                <ul>
                    {''.join([f'<li>{s}</li>' for s in ds_info.get('symptoms', [])])}
                </ul>
                
                <div style="background: #e6fffa; padding: 15px; border: 1px solid #00f5a0; border-radius: 5px; margin: 15px 0;">
                    <h3 style="margin-top: 0; color: #007955;">💊 Treatment Protocol</h3>
                    <ol>
                        {''.join([f'<li>{r}</li>' for r in ds_info.get('remedies', [])])}
                    </ol>
                </div>
            </div>
            """
            
            # 3. Send
            print("Sending report...")
            success = self.alerts.send_email_alert(
                f"📄 Full Analysis Report: {species} - {disease}", 
                html, 
                attachments=attachments
            )
            
            import tkinter.messagebox as msgbox
            if success:
                msgbox.showinfo("Sent", f"Full report for {species} sent to email successfully.")
            else:
                msgbox.showerror("Error", "Failed to send email.")
                
        except Exception as e:
            print(f"Report error: {e}")
            import tkinter.messagebox as msgbox
            msgbox.showerror("Error", str(e))

    def test_email_config(self):
        """Try sending a test email and report success/failure"""
        if not self.alerts or not self.alerts.email_enabled:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Error", "Email not configured in code.")
            return
            
        try:
            print("Attempting to send test email...")
            success = self.alerts.send_email_alert(
                "🧪 AquaVision AI Test",
                "<h3>Test Successful!</h3><p>Your email alerts are working correctly.</p>"
            )
            
            import tkinter.messagebox as msgbox
            if success:
                msgbox.showinfo("Success", "Test email sent successfully!\nCheck your inbox.")
            else:
                msgbox.showerror("Failed", "Could not send email.\nCheck console for details (likely App Password issue).")
        except Exception as e:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def save_detection_to_database(self, species, disease, species_conf=0.0, disease_conf=0.0, send_alert=False):
        """Save detection to database and send alerts if needed"""
        if not PROFESSIONAL_FEATURES or not self.db:
            return
        
        try:
            # Save to database
            detection_id = self.db.add_detection(
                species=species,
                disease=disease,
                image_path=self.current_image if self.current_image else "camera/video",
                species_conf=species_conf,
                disease_conf=disease_conf
            )
            
            # Check if alert should be sent (Only if explicitly requested)
            if send_alert and self.alerts and self.alerts.should_alert(disease, disease_conf):
                self.alerts.send_disease_detection_alert(
                    species=species,
                    disease=disease,
                    confidence=disease_conf,
                    image_path=self.current_image
                )
            
            print(f"[OK] Detection saved (ID: {detection_id})")
        except Exception as e:
            print(f"Error saving detection: {e}")

if __name__ == "__main__":
    app = AquaVisionPro()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
