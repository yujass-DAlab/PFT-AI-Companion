# 🫁 PFT AI Companion

### *Patient-Centered Spirometry Coaching & Preparation Tool*

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-5.0-green.svg)](https://gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Overview

The **PFT AI Companion** is a modular, patient-facing desktop application designed to help individuals practice and prepare for Pulmonary Function Tests (Spirometry). 

Unlike traditional passive reading materials, this tool uses real-time audio analysis and Text-to-Speech (TTS) coaching to guide users through the three critical steps of a spirometry maneuver:

1. **🌬️ Breathe In** – Maximize inhalation.
2. **💨 Blast Out** – Forceful, explosive exhalation.
3. **⏱️ Sustain** – Maintain the blow for at least 6 seconds.

The application evaluates the user's **Explosive Start (Amplitude)**, **Duration**, and **Airflow Stability**, providing immediate, personalized coaching feedback.

**⚠️ Clinical Disclaimer:** This tool is for **educational and preparation purposes only**. It does **not** diagnose lung conditions or replace professional clinical judgment.

---

## ✨ Key Features

- **📘 Educational Background:** Learn what to expect during a PFT with patient-friendly language.
- **🎮 Choose Your Path:** "Start Training" (unlimited practice) or "Skip to Live Test" (simulated real test).
- **🎙️ Real-Time Audio Analysis:** Uses your microphone to measure breath effort, duration, and stability.
- **🤖 AI Coaching Feedback:** Instant, actionable feedback after every attempt.
- **🗣️ Offline Voice Guidance:** Integrated Text-to-Speech (TTS) guides you hands-free through the steps.

---

## 🛠️ Tech Stack

| **Category** | **Technologies** |
| :--- | :--- |
| **Frontend/UI** | Gradio (Python) |
| **Audio Processing** | SciPy, NumPy |
| **Text-to-Speech** | pyttsx3 (Offline) |
| **Backend** | Pure Python (Modular Architecture) |

---

## 🚀 Installation & Local Setup

### Prerequisites
- Python 3.11+ installed.
- Working microphone.

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yujass-DAlab/PFT-AI-Companion.git
   cd PFT-AI-Companion

2. Install dependencies:
bash
pip install -r requirements.txt

3. Run the application:
bash
python app.py

5. Open your browser and go to: http://127.0.0.1:7860

📁 Project Architecture
The application is built with a clean, maintainable structure:

text
PFT-AI-Companion/
├── app.py                 # Main Gradio orchestrator
├── pages/                 # Individual UI modules (Background, Proclamation, Practice, Live)
├── utils/                 # Core logic (Audio Engine, UI Helpers)
└── requirements.txt       # Dependencies

👩‍⚕️ Patient Flow
Background: Read about the procedure.

Choose Experience: Decide to practice or take the simulated live test.

Practice/Training: Follow the 3 audio-guided steps. Click "Analyze" to get coaching.

Live Test: One-shot attempt, mimicking real clinical conditions.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🧠 New Section 1: Lessons Learned
(Add this after the Patient Flow section)

markdown
## 🧠 Lessons Learned
This project reinforced several important principles about building patient-facing healthcare tools:
- **Modularity Over Monoliths:** Splitting the application into `pages/` (UI) and `utils/` (core logic) saved hours of debugging. When the `Audio_Engine` needed tweaking, I didn’t have to search through a 500-line UI file.
- **Audio is Fickle:** Both Gradio’s audio component and `pyttsx3` have quirks. 
    - `pyttsx3` needs a **fresh engine instance** for every TTS call to avoid the "zombie" state where it stops speaking after the first prompt.
    - Gradio's `type="filepath"` (reading WAV files with `scipy`) proved more stable for feature extraction than `type="numpy"` when running repeated tests.
- **Simplicity Wins for UX:** The 3-step manual panel (Breathe In → Blast → Sustain) is far more intuitive and robust than trying to automatically detect the start and end of a blow. Users appreciate clear, self-paced controls.
- **Patient Language Matters:** Replacing technical terms (e.g., "sustain" → "keep blowing") and adding audio prompts made the tool more accessible. A patient should never have to read the screen while trying to blow out as hard as they can.
🔮 New Section 2: Future Developments
(Add this right after Lessons Learned)
🧠 New Section 3: Limitations
(I recommend placing this right after "Lessons Learned" and before "Future Developments" to create a natural flow: What I learned → What is missing → What is next).

markdown
## ⚠️ Limitations
While the PFT AI Companion is a powerful educational and coaching tool, it is **not** a medical device. Users and reviewers should be aware of the following limitations:
- **Audio Quality Dependency:** The feature extraction (explosiveness, duration, stability) relies entirely on the quality of the microphone input. Ambient noise, microphone sensitivity, and distance from the microphone can significantly impact the extracted metrics.
- **Surrogate Metrics Only:** The app measures **audio amplitude** and **duration**, which are reasonable surrogates for clinical effort. However, they do not replace the calibrated flow/volume sensors used in a real Pulmonary Function Test (which measure FEV1, FVC, etc.).
- **No Clinical Validation:** This application has not been formally validated in a clinical trial against standard spirometry equipment. It is designed for **patient preparation and education** to reduce anxiety, not for diagnostic screening.
- **Stability Metric Simplification:** The "Airflow Stability" score is a mathematical proxy based on the ratio of mean to peak amplitude. It helps coach users toward a smoother blow, but it does not perfectly reflect the nuanced airflow dynamics captured by a clinical plethysmograph.
- **Offline TTS Variability:** The voice prompts rely on your operating system's native speech engine (`pyttsx3`). Voice quality and the presence of specific voices vary between Windows, macOS, and Linux, which may slightly alter the user experience.
- **No Data Persistence:** This is a **stateless** local application. No attempts, scores, or user data are stored or logged between sessions.

markdown
## 🔮 Future Developments
While the current version is fully functional, here are the planned improvements for the next iteration:
- **Real-Time Breath Visualization:** Add a live Flow-Volume loop or bar chart that reacts to the microphone input during the blast.
- **Bluetooth Spirometer Integration:** Connect to hardware (e.g., MIR Spirobank) via Web Bluetooth for clinical-grade data, bypassing microphone limitations.
- **Session Logging & Reporting:** Generate a downloadable PDF summary of all practice attempts with timestamps and trends.
- **Additional PFT Modules:** Expand beyond Spirometry to include coaching for Lung Volumes (Body Plethysmography) and DLCO (Diffusing Capacity).
- **Multi-Language TTS:** Add support for Spanish and Mandarin to reach a broader patient population.
- AWS deployment. 
---

## 🙏 Acknowledgments
This project was developed with technical guidance and architectural support from AI language models, including **ChatGPT** and **DeepSeek**. Their contributions assisted in code structuring, debugging, modular design, and patient-friendly prompt engineering, enhancing the overall quality and completeness of this healthcare AI tool.

Special thanks to the open-source community for:
- **Gradio** – For the intuitive web UI framework.
- **pyttsx3** – For offline Text-to-Speech capabilities.
- **SciPy & NumPy** – For audio signal processing.

---

## 📸 Screenshots
*Here is a preview of the PFT AI Companion in action:*

  <<img width="1687" height="910" alt="PFT-AI-Companion-ChooseExperiencePage" src="https://github.com/user-attachments/assets/bec7ee6c-7c66-468e-a563-22e2ce821e94" />

  
  <<img width="1626" height="913" alt="PFT-AI-Companion-LivePage" src="https://github.com/user-attachments/assets/8119a192-157c-4e8a-a91c-f90a89ec7429" />

  <<<img width="1719" height="907" alt="PFT-AI-Companion-Practice" src="https://github.com/user-attachments/assets/b978f5eb-2dbd-4da6-97e2-d222c5c708dc" />
