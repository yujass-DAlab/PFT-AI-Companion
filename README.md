# 🫁 PFT AI Companion (V2)

### *Patient-Centered Spirometry Coaching & Preparation Tool — Now Live on AWS!*

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-5.0-green.svg)](https://gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AWS](https://img.shields.io/badge/Live%20Demo-AWS-orange.svg)](http://52.15.208.206:7860)

---

## 🚀 Live Demo

**Try the app right now:**  
👉 [http://52.15.208.206:7860](http://52.15.208.206:7860)

*Note: The microphone feature works best on `localhost` (HTTPS required for public IPs). All other features—coaching, feedback, progress tracking—work flawlessly on the cloud.*

---

## 📖 Overview
This project is a Minimum Viable Product (MVP) for patient-centered spirometry coaching. 

It focuses on the three most critical breathing maneuvers, providing real-time audio feedback and offline voice guidance to help patients build confidence before their actual Pulmonary Function Test.

The **PFT AI Companion V2** is a modular, patient-facing desktop application designed to help individuals practice and prepare for Pulmonary Function Tests (Spirometry). 

Unlike traditional passive reading materials, this tool uses real-time audio analysis and Text-to-Speech (TTS) coaching to guide users through the three critical steps of a spirometry maneuver:

1. **🌬️ Breathe In Deeply** – Maximize inhalation.
2. **💨 Blast Out** – Forceful, explosive exhalation.
3. **⏱️ Sustain** – Keep blowing for at least 6 seconds.

The application evaluates the user's **Explosive Start (Amplitude)**, **Duration**, and **Airflow Stability**, providing immediate, personalized coaching feedback.

**⚠️ Clinical Disclaimer:** This tool is for **educational and preparation purposes only**. It does **not** diagnose lung conditions or replace professional clinical judgment.

---

## ✨ Key Features (V2)

- **📘 Educational Background:** Learn what to expect during a PFT with patient-friendly language.
- **🎮 Choose Your Path:** "Start Training" (unlimited practice) or "Skip to Live Test" (simulated real test).
- **🎙️ Real-Time Audio Analysis:** Uses your microphone to measure breath effort, duration, and stability.
- **🤖 Weighted AI Coaching:** Blast effort is weighted 1.5x (clinically, FEV1 is the most critical metric).
- **📊 Step-Based Progress:** Users see exactly where they are (`Step 1 of 4`, `Step 2 of 4`, etc.).
- **👤 Human Therapist Option:** A dedicated button allows users to request a real therapist during the live test.
- **🗣️ Offline Voice Guidance:** Integrated Text-to-Speech (TTS) guides you hands-free through the steps.

---

## 🛠️ Tech Stack

| **Category** | **Technologies** |
| :--- | :--- |
| **Frontend/UI** | Gradio (Python) |
| **Audio Processing** | SciPy, NumPy |
| **Text-to-Speech** | pyttsx3 (Offline) |
| **Backend** | Pure Python (Modular Architecture) |
| **Deployment** | Docker, AWS ECR, AWS EC2 |

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
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app_v2.py
   ```

4. **Open your browser** and go to: `http://127.0.0.1:7862` (or the port shown in the terminal).

---

## 📁 Project Architecture

The application is built with a clean, maintainable structure:

```
PFT-AI-Companion/
├── app_v2.py             # Main Gradio orchestrator
├── pages/                # Individual UI modules (Background, Proclamation, Practice, Live)
├── utils/                # Core logic (Audio Engine, UI Helpers)
└── requirements.txt      # Dependencies
```

---

## 👩‍⚕️ Patient Flow

1. **Background:** Read about the procedure and common terms.
2. **Choose Experience:** Decide to practice or take the simulated live test.
3. **Practice/Training:** Follow the 3 audio-guided steps. Click "Analyze" to get coaching.
4. **Live Test:** One-shot attempt, mimicking real clinical conditions. You can request a human therapist at any time.

---

## 🧠 Lessons Learned (V2 Deployment)

This project reinforced several important principles about building and deploying patient-facing healthcare tools:

- **TTS is Fickle:** `pyttsx3` needs a **fresh engine instance** for every call to avoid the "zombie" state where it stops speaking after the first prompt.
- **Audio Libraries Are Heavy:** The inclusion of `ffmpeg`, `scipy`, and `gradio` makes the Docker image ~3.27 GB (compressed). Plan your cloud storage accordingly.
- **AWS Disk Space is Limited:** A standard EC2 `t3.micro` has only 8 GB of storage. For large Gradio apps, expand the EBS volume to 20 GB before pulling the image.
- **Microphone & HTTPS:** Browsers block microphone access on HTTP public IPs. The mic works perfectly on `localhost`, but for cloud deployment, SSL/HTTPS is required for full functionality.
- **Threading is Essential:** TTS calls must run in a separate daemon thread to prevent the Gradio UI from freezing.

---

## ⚠️ Limitations

While the PFT AI Companion is a powerful educational and coaching tool, it is **not** a medical device. Users and reviewers should be aware of the following limitations:

- **Audio Quality Dependency:** The feature extraction relies entirely on the quality of the microphone input.
- **Surrogate Metrics Only:** The app measures **audio amplitude** and **duration**, which are reasonable surrogates for clinical effort. They do not replace calibrated flow/volume sensors (FEV1, FVC).
- **No Clinical Validation:** This application has not been formally validated against standard spirometry equipment.
- **HTTPS Requirement:** The microphone will not work on public HTTP IPs due to browser security policies.

---

## 🔮 Future Developments

- **Real-Time Breath Visualization:** Add a live Flow-Volume loop.
- **Bluetooth Spirometer Integration:** Connect to hardware (e.g., MIR Spirobank).
- **Session Logging & Reporting:** Generate downloadable PDF summaries.
- **HTTPS Setup:** Add a free Let's Encrypt SSL certificate for full microphone support on AWS.

---

## 🙏 Acknowledgments

This project was developed with technical guidance and architectural support from AI language models, including **ChatGPT** and **DeepSeek**. Their contributions assisted in code structuring, debugging, modular design, and patient-friendly prompt engineering.

Special thanks to the open-source community for:
- **Gradio** – For the intuitive web UI framework.
- **pyttsx3** – For offline Text-to-Speech capabilities.
- **SciPy & NumPy** – For audio signal processing.

---

## 📸 Screenshots

*Here is a preview of the PFT AI Companion V2 in action:*

<<img width="700" height="600" alt="v2FLive" src="https://github.com/user-attachments/assets/0ce12375-8e29-4bc3-b12f-aa7490497a2e" />

<img width="700" height="600" alt="v2FPractice" src="https://github.com/user-attachments/assets/b05ee1fe-12d4-4bba-9cf7-84f4e46bc6c2" />

<img width="700" height="600" alt="v2FChooseExperience" src="https://github.com/user-attachments/assets/a4708d90-a0db-4466-a29b-747dca2b357f" />

<img width="700" height="600" alt="v2FBackground" src="https://github.com/user-attachments/assets/e0b74cdc-807b-4975-ad41-e59b5094b663" />


---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Built with ❤️ for patient empowerment in respiratory health.
