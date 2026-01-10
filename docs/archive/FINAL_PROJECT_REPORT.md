# 📄 AQUAVISION AI – FINAL PROJECT REPORT
**Date:** January 9, 2026  
**Author:** Mohammed Amaan  
**Version:** 3.0 (Professional Edition)

---

## 🚀 1. Executive Summary
**AquaVision AI** is a comprehensive, deep-learning-based software solution designed to detect and classify diseases in freshwater fish. Addressing the critical need for early diagnosis in aquaculture, this system leverages advanced Computer Vision to identify 7 distinct health conditions with **76.55% accuracy** and **88% precision**.

The project successfully bridges the gap between complex AI research and practical application by delivering a fully functional desktop application capable of **real-time inference**, **explainable diagnostics (Grad-CAM)**, and **automated alerts**.

---

## 🎯 2. Project Objectives & Scope
The primary goal was to build a system that is:
*   **Accurate:** Reliability detecting diseases to prevent economic loss.
*   **Accessible:** Running efficiently on standard hardware (Edge-AI ready).
*   **Explainable:** Providing visual evidence for why a diagnosis was made.
*   **Operational:** Including features for long-term health monitoring (History, Database).

### Scope of Detection (7 Classes)
| Class | Type | Status |
| :--- | :--- | :--- |
| **Healthy Fish** | N/A | ✅ Detected |
| **Aeromoniasis** | Bacterial | 🔴 Detected |
| **Gill Disease** | Bacterial | 🔴 Detected |
| **Red Disease** | Bacterial | 🔴 Detected |
| **Saprolegniasis** | Fungal | 🟡 Detected |
| **Parasitic Disease** | Parasitic | 🟠 Detected |
| **White Tail Disease** | Viral | 🔵 Detected |

---

## 🛠 3. Technical Architecture

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

## ⚡ 4. Key Features Implemented

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

## 📊 5. Performance Metrics

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

## 🔮 6. Future Scope
*   **Mobile App:** Porting the TFLite model to a dedicated Android/iOS app.
*   **Cloud Integration:** Uploading detection history to a cloud dashboard for remote monitoring of multiple farms.
*   **Treatment Recommendations:** Integrating a chatbot API (like the one prototyped) to suggest specific medicines based on the disease found.

---

## ✅ 7. Conclusion
AquaVision AI is no longer just a prototype. It is a **full-stack, production-ready desktop application**. By combining state-of-the-art Deep Learning with robust software engineering practices (Database, GUI, Alerts), it provides a tangible solution to real-world aquaculture challenges.

***
**Project Status:** COMPLETE  
**Code Repository:** Local  
