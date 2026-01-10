
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Final Year Project: Fish Disease Detection System', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()

    def add_image(self, image_path, title, w=100):
        if os.path.exists(image_path):
            self.ln(5)
            self.set_font('Arial', 'I', 10)
            self.cell(0, 5, title, 0, 1, 'C')
            # Center image
            x = (self.w - w) / 2
            self.image(image_path, x=x, w=w)
            self.ln(5)
        else:
            self.chapter_body(f"[Image placeholder: {title} - File not found]")

def create_pdf():
    pdf = PDF()
    pdf.add_page()
    
    # 1. Introduction
    pdf.chapter_title("1. Introduction")
    pdf.chapter_body(
        "For your Final Year Project, you are presenting 'AquaVision AI', a comprehensive system designed "
        "to detect diseases in freshwater fish using Deep Learning. The project addresses the critical issue "
        "of disease outbreaks in aquaculture which cause significant economic losses."
    )

    # 2. Problem Statement
    pdf.chapter_title("2. Problem Statement")
    pdf.chapter_body(
        "- Manual disease detection is slow, error-prone, and requires experts.\n"
        "- Late detection leads to rapid disease spread and high mortality.\n"
        "- Lack of accessible tools for farmers to diagnose fish health on-site."
    )

    # 3. Objectives
    pdf.chapter_title("3. Project Objectives")
    pdf.chapter_body(
        "- Develop an accurate AI model (>75% accuracy) to classify 7 distinct fish conditions.\n"
        "- Implement 'Explainable AI' (Grad-CAM) to visualize disease symptoms, building trust.\n"
        "- Create a user-friendly Desktop Application for real-time diagnosis.\n"
        "- Ensure the system can run offline on edge devices (low latency)."
    )

    # 4. Methodology & Key Features
    pdf.chapter_title("4. Methodology & Technology")
    pdf.chapter_body(
        "We utilized Transfer Learning with the MobileNetV2 architecture, pre-trained on ImageNet, "
        "fine-tuned on our dataset of 2,400+ fish images. \n\n"
        "Key Technologies:\n"
        "- Framework: TensorFlow/Keras\n"
        "- GUI: CustomTkinter (Python)\n"
        "- Database: SQLite (for tracking history)\n"
        "- Interpretability: Grad-CAM (Gradient-weighted Class Activation Mapping)"
    )

    # 5. Visual Evidence (Explainability)
    pdf.add_image('c:/Fish-Disease-Detection/results/gradcam_visualization.png', 'Figure 1: Grad-CAM Visualization (AI "Vision")')
    pdf.chapter_body(
        "The image above demonstrates the system's explainability. The heatmap highlights the specific "
        "regions of the fish (e.g., gills, tail) that the AI used to make its diagnosis, helping users "
        "verify the result."
    )
    
    pdf.add_page()

    # 6. Results
    pdf.chapter_title("5. Performance Results")
    pdf.chapter_body(
        "The model achieved strong performance metrics on the test set:\n"
        "- Overall Accuracy: 76.55%\n"
        "- Precision: 88.42% (Minimizing false alarms)\n"
        "- Inference Speed: <1 second per image (Real-time capability)\n"
        "- Model Size: 2.40 MB (Optimized for deployment)"
    )

    # 7. Visual Evidence (Confusion Matrix)
    pdf.add_image('c:/Fish-Disease-Detection/results/confusion_matrix.png', 'Figure 2: Confusion Matrix')
    
    # 8. Conclusion
    pdf.chapter_title("6. Conclusion")
    pdf.chapter_body(
        "AquaVision AI successfully automates fish disease detection. It empowers farmers with expert-level "
        "diagnostics without the need for constant internet connectivity. The inclusion of Grad-CAM "
        "transparency and a robust history tracking system makes it a professional-grade tool suitable for "
        "real-world aquaculture applications."
    )

    # 9. Presentation Tips
    pdf.chapter_title("7. Presentation Tips")
    pdf.chapter_body(
        "- Live Demo: Show the 'Real-time Camera' feature during your presentation if possible.\n"
        "- Highlight user benefits: 'Saves money', 'Saves time', 'Easy to use'.\n"
        "- Emphasize 'Explainable AI': Judges love knowing *why* the AI made a decision."
    )

    output_path = 'c:/Fish-Disease-Detection/Fish_Disease_Detection_FYP_Notes.pdf'
    pdf.output(output_path)
    print(f"PDF generated successfully at: {output_path}")

if __name__ == '__main__':
    create_pdf()
