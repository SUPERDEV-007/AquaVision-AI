
import markdown
import os

# Content extracted from the FINAL_PROJECT_REPORT.md
content_markdown_raw = """
# AQUAVISION AI – FINAL PROJECT REPORT
**Date:** January 9, 2026  
**Author:** Mohammed Amaan  
**Version:** 3.0 (Professional Edition)

---

## 1. Executive Summary
**AquaVision AI** is a comprehensive, deep-learning-based software solution designed to detect and classify diseases in freshwater fish. Addressing the critical need for early diagnosis in aquaculture, this system leverages advanced Computer Vision to identify 7 distinct health conditions with **76.55% accuracy** and **88% precision**.

The project successfully bridges the gap between complex AI research and practical application by delivering a fully functional desktop application capable of **real-time inference**, **explainable diagnostics (Grad-CAM)**, and **automated alerts**.

---

## 2. Project Objectives & Scope
The primary goal was to build a system that is:
*   **Accurate:** Reliability detecting diseases to prevent economic loss.
*   **Accessible:** Running efficiently on standard hardware (Edge-AI ready).
*   **Explainable:** Providing visual evidence for why a diagnosis was made.
*   **Operational:** Including features for long-term health monitoring (History, Database).

### Scope of Detection (7 Classes)
| Class | Type | Status |
| :--- | :--- | :--- |
| **Healthy Fish** | N/A | Detected |
| **Aeromoniasis** | Bacterial | Detected |
| **Gill Disease** | Bacterial | Detected |
| **Red Disease** | Bacterial | Detected |
| **Saprolegniasis** | Fungal | Detected |
| **Parasitic Disease** | Parasitic | Detected |
| **White Tail Disease** | Viral | Detected |

---

## 3. Technical Architecture

### A. Tech Stack
*   **Language:** Python 3.10+
*   **Framework:** TensorFlow / Keras (Deep Learning), OpenCV (Vision)
*   **GUI:** CustomTkinter (Modern Desktop Interface)
*   **Database:** SQLite (Local storage for privacy & speed)
*   **Utils:** Pandas, NumPy, Plyer (Notifications), SMTPlib (Email)

### B. The AI Model (MobileNetV2)
We utilized **Transfer Learning** with the **MobileNetV2** architecture.
*   **Why MobileNetV2?** It is optimized for mobile & edge devices, offering the perfect balance between speed and accuracy.
*   **Custom Head:** Added Global Average Pooling, Dropout (0.3) for regularization, and a Softmax Dense layer for 7-class classification.
*   **Optimization:** The model was quantified to **INT8 TFLite format**, reducing size to just **2.40 MB** without losing significant accuracy.

### C. Explainable AI (Grad-CAM)
To trust the AI, users need to see *what* it is looking at. We implemented **Gradient-weighted Class Activation Mapping (Grad-CAM)**.
*   **How it works:** It extracts gradients from the final convolutional layer to highlight important regions.
*   **Result:** A heatmap overlay shows red/yellow zones where signs of disease (bloody spots, white patches) are detected.

---

## 4. Key Features Implemented

### 1. Real-Time Detection
*   **Live Camera Feed:** Processes video input at ~30 FPS with inference running on keyframes.
*   **Video Analysis:** Supports uploading pre-recorded videos for batched analysis.

### 2. Multi-Fish Detection
*   Advanced logic to identify and box **multiple fish** in a single frame.
*   Each fish is analyzed individually for disease status.

### 3. Smart Alert System
*   **Desktop Notifications:** Instant pop-ups when a disease is found.
*   **Email Alerts:** Automated emails sent to farm owners with details of the detection (Species, Disease, Confidence Score).

### 4. Digital Health Log (History)
*   Every detection is automatically saved to a local **SQLite database**.
*   Users can view a chronological history of scans to track disease outbreaks over time.

---

## 5. Performance Metrics

### Test Set Evaluation (469 Images)
*   **Overall Accuracy:** **76.55%**
*   **Precision:** **88.42%** (Very low false positives)
*   **Recall:** 58.64%
*   **F1-Score:** 76.41%

### Deployment Stats
*   **Model Size:** 2.40 MB (Ultra-lightweight)
*   **Inference Time:** < 500ms (CPU)
*   **Memory Usage:** < 150 MB RAM

---

## 6. Future Scope
*   **Mobile App:** Porting the TFLite model to a dedicated Android/iOS app.
*   **Cloud Integration:** Uploading detection history to a cloud dashboard for remote monitoring of multiple farms.
*   **Treatment Recommendations:** Integrating a chatbot API (like the one prototyped) to suggest specific medicines based on the disease found.

---

## 7. Conclusion
AquaVision AI is no longer just a prototype. It is a **full-stack, production-ready desktop application**. By combining state-of-the-art Deep Learning with robust software engineering practices (Database, GUI, Alerts), it provides a tangible solution to real-world aquaculture challenges.

***
**Project Status:** COMPLETE  
**Code Repository:** Local  
"""

# HTML Template with Professional Styling
html_template = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    @page {{
        size: A4;
        margin: 2.54cm;
    }}
    body {{
        font-family: "Times New Roman", Times, serif;
        font-size: 12pt;
        line-height: 1.5;
        color: #000;
        max-width: 21cm;
        margin: 0 auto;
        padding: 2cm 0;
        background-color: #fff;
    }}
    h1 {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 24pt;
        color: #2E4053;
        text-align: center;
        margin-bottom: 0.5cm;
        border-bottom: 2px solid #2E4053;
        padding-bottom: 0.2cm;
    }}
    h2 {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 16pt;
        color: #2874A6;
        margin-top: 1.5cm;
        margin-bottom: 0.5cm;
        border-bottom: 1px solid #ddd;
    }}
    h3 {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 14pt;
        color: #5D6D7E;
        margin-top: 1cm;
        margin-bottom: 0.3cm;
    }}
    p {{
        text-align: justify;
        margin-bottom: 0.5cm;
    }}
    strong {{
        color: #1B2631;
    }}
    ul, ol {{
        margin-bottom: 0.5cm;
        padding-left: 1cm;
    }}
    li {{
        margin-bottom: 0.2cm;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 1cm 0;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 11pt;
    }}
    th, td {{
        border: 1px solid #ccc;
        padding: 8px 12px;
        text-align: left;
    }}
    th {{
        background-color: #F2F4F4;
        font-weight: bold;
    }}
    hr {{
        border: 0;
        border-top: 1px solid #eee;
        margin: 1cm 0;
    }}
    .meta-info {{
        text-align: center;
        font-style: italic;
        color: #555;
        margin-bottom: 2cm;
    }}
    @media print {{
        body {{
            width: 100%;
            margin: 0;
            padding: 0;
        }}
        h2 {{
            page-break-before: auto;
        }}
        tr {{
            page-break-inside: avoid;
        }}
    }}
</style>
</head>
<body>
{content}
</body>
</html>
"""

# Simple Markdown parser for this specific content structure
# Note: Using a library would be better, but 'markdown' might not be installed. 
# I'll implement a simple one or use 'markdown' if available. 
# Since I cannot guarantee 'markdown' lib is present in user environment, 
# I will output the raw text pre-formatted into the HTML body using the 'markdown' lib if available, 
# otherwise I will use a simple regex replacement.
# WAIT - I can just write the content as HTML directly to be safe.

html_content_body = """
<h1>AQUAVISION AI – FINAL PROJECT REPORT</h1>
<div class="meta-info">
    <p><strong>Date:</strong> January 9, 2026<br>
    <strong>Author:</strong> Mohammed Amaan<br>
    <strong>Version:</strong> 3.0 (Professional Edition)</p>
</div>

<h2>1. Executive Summary</h2>
<p><strong>AquaVision AI</strong> is a comprehensive, deep-learning-based software solution designed to detect and classify diseases in freshwater fish. Addressing the critical need for early diagnosis in aquaculture, this system leverages advanced Computer Vision to identify 7 distinct health conditions with <strong>76.55% accuracy</strong> and <strong>88% precision</strong>.</p>
<p>The project successfully bridges the gap between complex AI research and practical application by delivering a fully functional desktop application capable of <strong>real-time inference</strong>, <strong>explainable diagnostics (Grad-CAM)</strong>, and <strong>automated alerts</strong>.</p>

<h2>2. Project Objectives & Scope</h2>
<p>The primary goal was to build a system that is:</p>
<ul>
    <li><strong>Accurate:</strong> Reliability detecting diseases to prevent economic loss.</li>
    <li><strong>Accessible:</strong> Running efficiently on standard hardware (Edge-AI ready).</li>
    <li><strong>Explainable:</strong> Providing visual evidence for why a diagnosis was made.</li>
    <li><strong>Operational:</strong> Including features for long-term health monitoring (History, Database).</li>
</ul>

<h3>Scope of Detection (7 Classes)</h3>
<table>
    <tr><th>Class</th><th>Type</th><th>Status</th></tr>
    <tr><td><strong>Healthy Fish</strong></td><td>N/A</td><td>Detected</td></tr>
    <tr><td><strong>Aeromoniasis</strong></td><td>Bacterial</td><td>Detected</td></tr>
    <tr><td><strong>Gill Disease</strong></td><td>Bacterial</td><td>Detected</td></tr>
    <tr><td><strong>Red Disease</strong></td><td>Bacterial</td><td>Detected</td></tr>
    <tr><td><strong>Saprolegniasis</strong></td><td>Fungal</td><td>Detected</td></tr>
    <tr><td><strong>Parasitic Disease</strong></td><td>Parasitic</td><td>Detected</td></tr>
    <tr><td><strong>White Tail Disease</strong></td><td>Viral</td><td>Detected</td></tr>
</table>

<h2>3. Technical Architecture</h2>

<h3>A. Tech Stack</h3>
<ul>
    <li><strong>Language:</strong> Python 3.10+</li>
    <li><strong>Framework:</strong> TensorFlow / Keras (Deep Learning), OpenCV (Vision)</li>
    <li><strong>GUI:</strong> CustomTkinter (Modern Desktop Interface)</li>
    <li><strong>Database:</strong> SQLite (Local storage for privacy & speed)</li>
    <li><strong>Utils:</strong> Pandas, NumPy, Plyer (Notifications), SMTPlib (Email)</li>
</ul>

<h3>B. The AI Model (MobileNetV2)</h3>
<p>We utilized <strong>Transfer Learning</strong> with the <strong>MobileNetV2</strong> architecture.</p>
<ul>
    <li><strong>Why MobileNetV2?</strong> It is optimized for mobile & edge devices, offering the perfect balance between speed and accuracy.</li>
    <li><strong>Custom Head:</strong> Added Global Average Pooling, Dropout (0.3) for regularization, and a Softmax Dense layer for 7-class classification.</li>
    <li><strong>Optimization:</strong> The model was quantified to <strong>INT8 TFLite format</strong>, reducing size to just <strong>2.40 MB</strong> without losing significant accuracy.</li>
</ul>

<h3>C. Explainable AI (Grad-CAM)</h3>
<p>To trust the AI, users need to see <em>what</em> it is looking at. We implemented <strong>Gradient-weighted Class Activation Mapping (Grad-CAM)</strong>.</p>
<ul>
    <li><strong>How it works:</strong> It extracts gradients from the final convolutional layer to highlight important regions.</li>
    <li><strong>Result:</strong> A heatmap overlay shows red/yellow zones where signs of disease (bloody spots, white patches) are detected.</li>
</ul>

<h2>4. Key Features Implemented</h2>

<h3>1. Real-Time Detection</h3>
<ul>
    <li><strong>Live Camera Feed:</strong> Processes video input at ~30 FPS with inference running on keyframes.</li>
    <li><strong>Video Analysis:</strong> Supports uploading pre-recorded videos for batched analysis.</li>
</ul>

<h3>2. Multi-Fish Detection</h3>
<ul>
    <li>Advanced logic to identify and box <strong>multiple fish</strong> in a single frame.</li>
    <li>Each fish is analyzed individually for disease status.</li>
</ul>

<h3>3. Smart Alert System</h3>
<ul>
    <li><strong>Desktop Notifications:</strong> Instant pop-ups when a disease is found.</li>
    <li><strong>Email Alerts:</strong> Automated emails sent to farm owners with details of the detection (Species, Disease, Confidence Score).</li>
</ul>

<h3>4. Digital Health Log (History)</h3>
<ul>
    <li>Every detection is automatically saved to a local <strong>SQLite database</strong>.</li>
    <li>Users can view a chronological history of scans to track disease outbreaks over time.</li>
</ul>

<h2>5. Performance Metrics</h2>

<h3>Test Set Evaluation (469 Images)</h3>
<ul>
    <li><strong>Overall Accuracy:</strong> <strong>76.55%</strong></li>
    <li><strong>Precision:</strong> <strong>88.42%</strong> (Very low false positives)</li>
    <li><strong>Recall:</strong> 58.64%</li>
    <li><strong>F1-Score:</strong> 76.41%</li>
</ul>

<h3>Deployment Stats</h3>
<ul>
    <li><strong>Model Size:</strong> 2.40 MB (Ultra-lightweight)</li>
    <li><strong>Inference Time:</strong> < 500ms (CPU)</li>
    <li><strong>Memory Usage:</strong> < 150 MB RAM</li>
</ul>

<h2>6. Future Scope</h2>
<ul>
    <li><strong>Mobile App:</strong> Porting the TFLite model to a dedicated Android/iOS app.</li>
    <li><strong>Cloud Integration:</strong> Uploading detection history to a cloud dashboard for remote monitoring of multiple farms.</li>
    <li><strong>Treatment Recommendations:</strong> Integrating a chatbot API (like the one prototyped) to suggest specific medicines based on the disease found.</li>
</ul>

<h2>7. Conclusion</h2>
<p>AquaVision AI is no longer just a prototype. It is a <strong>full-stack, production-ready desktop application</strong>. By combining state-of-the-art Deep Learning with robust software engineering practices (Database, GUI, Alerts), it provides a tangible solution to real-world aquaculture challenges.</p>

<hr>
<p style="text-align: center;"><strong>Project Status:</strong> COMPLETE | <strong>Code Repository:</strong> Local</p>
"""

full_html = html_template.format(content=html_content_body)

with open("Project_Report_Printable.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Report generated: Project_Report_Printable.html")
