# AI Spirometry Companion (V4 – PWA Edition)

**One page. Two modes. All stats.**

A Progressive Web App for practicing Pulmonary Function Tests (PFT) with AI coaching, real‑time scoring, and live/practice modes.

## ✨ Features
- **Practice & Live modes** – instant switching with zero latency
- **Instant effort scoring** – explosion, duration, stability
- **AI voice coaching** – step‑by‑step guidance (gTTS)
- **PWA installable** – works offline after first load
- **Unified attempt chart** – track progress across modes
- **Improved UI** – larger gauges, red clear button, visible dark text

## 🚀 Run locally

```bash
pip install -r requirements.txt
python spirometry_v4_pwa.py# 🫁 PFT AI Companion (V3)
🐳 Run with Docker
bash
docker build -t spirometry-pwa .
docker run -d -p 7864:7863 --name spirometry-app -e PYTHONUNBUFFERED=1 spirometry-pwa
☁️ AWS Deployment: 
URL: http://18.225.32.182:7864
Built for Amazon ECR + EC2. See Dockerfile for details.

📄 License
Educational purposes only – not a substitute for clinical judgment.



### *A Patient‑Centered Spirometry Coaching & Preparation Tool*

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-5.0-green.svg)](https://gradio.app/)
[![Plotly](https://img.shields.io/badge/Plotly-6.0-purple.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AWS](https://img.shields.io/badge/Live%20Demo-AWS-orange.svg)](http://3.15.171.219:7863)

---

## 🚀 Live Demo

**Try the app right now:**  
👉 [http://18.225.32.182:7864](http://18.225.32.182:7864)

*(Microphone requires HTTPS – full functionality works on localhost. All other features work flawlessly on AWS).*

---

## 📖 Overview

The **PFT AI Companion V4** is a **unified, single‑page application** designed to help patients practice and prepare for Pulmonary Function Tests (Spirometry). It combines **Practice** and **Live Test** modes into one clean interface, using real‑time audio analysis and cloud‑compatible Text‑to‑Speech to guide users through the critical steps of a spirometry maneuver:

1. **🌬️ Breathe In Deeply** – Maximise inhalation.
2. **💨 Blast Out** – Forceful, explosive exhalation.
3. **⏱️ Sustain** – Keep blowing for at least 6 seconds.

The app evaluates **Explosive Start (amplitude)**, **Duration**, and **Airflow Stability**, providing immediate, personalised coaching feedback and a **colour‑coded bar chart** with a passing line at 80%.

**⚠️ Clinical Disclaimer:** This tool is for **educational and preparation purposes only**. It does **not** diagnose lung conditions or replace professional clinical judgment.

---

## ✨ Key Features (V4)

- **📘 Collapsible "About This App"** – Background, FEV₁, DLCO, PFT, and tips – all hidden until you need them.
- **🎮 Two Modes in One Page** – *Practice* (unlimited attempts) and *Live* (3‑out‑of‑8 rule, auto‑finishes).
- **🎙️ Real‑Time Audio Analysis** – Uses your microphone to measure breath effort, duration, and stability.
- **🗣️ Cloud‑Ready Voice Prompts** – Switched from `pyttsx3` to `gTTS` – works on Windows, Linux, and AWS.
- **📊 Interactive Bar Chart** – Built with Plotly: fixed 0–100 Y‑axis, colour‑coded bars (Practice 🟠 / Live 🟣), and a dashed **Pass** line at 80%.
- **📈 Attempt History & Trends** – Track your progress with a summary card and a numbered trend list (UP/DOWN/SAME arrows).
- **🔄 Session Controls** – Reset Live session or clear all history with one click.
- **☁️ Dockerised & Deployed** – Runs on AWS EC2 behind a Docker container.

---

## 🛠️ Tech Stack

| **Category** | **Technologies** |
| :--- | :--- |
| **Frontend/UI** | Gradio 5.0 |
| **Audio Processing** | SciPy, NumPy |
| **Text‑to‑Speech** | gTTS (Google Text‑to‑Speech) |
| **Charts** | Plotly, Pandas |
| **Backend** | Pure Python |
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
   
2. Install dependencies:
bash
pip install -r requirements.txt

4. Run the application:
bash
python spirometry_v4.py
Open your browser and go to: http://127.0.0.1:7864.

📁 Project Structure
V4 is a single‑file application – all logic is contained in spirometry_v4.py.
The repository also includes:

text
PFT-AI-Companion/
├── spirometry_v4.py       # Main application (unified single page)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container build instructions
├── .dockerignore          # Files to exclude from the Docker image
└── README.md              # This file

👩‍⚕️ User Flow
Choose a mode (Practice or Live) – the coach voice plays automatically.

Click the Record button (start/stop toggle) – blow when you hear "BLAST out!".

Score appears instantly – gauge, bar chart, and detailed summary update.

Continue – in Live mode, the app tracks attempts and auto‑finishes after 3 passing blows (≥80%) or 8 total attempts.

🧠 The Journey: From V1 to V3
Version	Focus	                                Key Change
V1	Single‑page prototype	Basic audio analysis + pyttsx3 TTS (Windows only).
V2	Modular architecture	Split UI (pages/) and logic (utils/). Added Live mode and therapist button.
V3	Unified single page	Removed pages/ and utils/ – everything in one file. Switched to gTTS for cloud compatibility. Added Plotly charts, fixed Y‑axis, and added a passing line. Deployed to AWS.
V4            Fixed latency                          Fixed mode switch latency, improved UI, added PWA capacity. 
⚠️ Limitations
Microphone requires HTTPS – on public IPs, the mic will not work over HTTP. All other features (coaching, scoring, charts) work perfectly.

Surrogate metrics only – the app measures audio amplitude and duration, not calibrated flow/volume (FEV₁, FVC).

No clinical validation – this is a coaching tool, not a diagnostic device.

Dependency on internet – gTTS needs an active internet connection to generate voice prompts.

🔮 Future Developments (V5+)
HTTPS + SSL – Add a free Let's Encrypt certificate to enable microphone on AWS.

Real‑time Flow‑Volume loop – visualise your breath as you blow.

Session history storage – save attempts to a database and generate PDF reports.

Multi‑language support – Spanish, Mandarin, etc.

🙏 Acknowledgments
This project was developed with technical guidance from AI language models, including ChatGPT and DeepSeek. Their contributions assisted in code structuring, debugging, modular design, and patient‑friendly prompt engineering.

Special thanks to the open‑source community for:

Gradio – for the intuitive web UI framework.

gTTS – for cloud‑compatible Text‑to‑Speech.

Plotly – for beautiful, interactive charts.

SciPy & NumPy – for audio signal processing.

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

Built with ❤️ for patient empowerment in respiratory health.
---

## 📸 Screenshots

### 🖥️ Unified Interface (V4)
The new single‑page layout puts everything – Practice/Live modes, scoring, and history – on one screen, reducing clutter and making navigation intuitive.

![<img width="713" height="921" alt="v3overall" src="https://github.com/user-attachments/assets/4b09ba91-b809-4da2-a6a6-80b435ab6644" />


---

### 📊 Interactive Dashboard
The Performance Dashboard includes a colour‑coded gauge, a Plotly bar chart with a fixed 0–100 Y‑axis, and a passing line at 80%.

![<img width="671" height="764" alt="v3blank" src="https://github.com/user-attachments/assets/5130c6a8-f7e4-4315-971c-a439d8c62365" />

---

### ☁️ AWS Deployment
The app is containerised with Docker and deployed on AWS EC2 – accessible from anywhere.

!<img width="1868" height="1027" alt="AWS-2-App" src="https://github.com/user-attachments/assets/c216ff84-2e4a-4325-911d-ee5e661b0413" />

