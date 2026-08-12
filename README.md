# AI Spirometry Companion (V4 – PWA Edition)

**One page. Two modes. All stats.**

A Progressive Web App for practicing Pulmonary Function Tests (PFT) with AI coaching, real‑time scoring, and live/practice modes.

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-5.0-green.svg)](https://gradio.app/)
[![Plotly](https://img.shields.io/badge/Plotly-6.0-purple.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AWS](https://img.shields.io/badge/Live%20Demo-AWS-orange.svg)](http://18.225.32.182:7864)

---

## 🚀 Live Demo

👉 [http://18.225.32.182:7864](http://18.225.32.182:7864)

> ⚠️ Microphone requires HTTPS – on public IPs, the mic will not work over HTTP. All other features (coaching, scoring, charts) work perfectly.

---

## 📖 Overview

The **PFT AI Companion V4** is a unified, single‑page application that helps patients practice and prepare for Spirometry. It combines **Practice** and **Live Test** modes into one interface, using real‑time audio analysis and cloud‑based Text‑to‑Speech to guide users through the critical steps:

1. 🌬️ **Breathe In Deeply** – maximise inhalation.
2. 💨 **Blast Out** – forceful, explosive exhalation.
3. ⏱️ **Sustain** – keep blowing for at least 6 seconds.

The app evaluates **Explosive Start (amplitude)**, **Duration**, and **Airflow Stability**, giving instant coaching feedback and a colour‑coded bar chart with a passing line at 80%.

**⚠️ Clinical Disclaimer:** This tool is for **educational and preparation purposes only**. It does **not** diagnose lung conditions or replace professional clinical judgment.

---

## ✨ Key Features

- 📘 **Collapsible "About" section** – background, FEV₁, DLCO, PFT, and tips.
- 🎮 **Two modes in one page** – *Practice* (unlimited) and *Live* (3‑out‑of‑8 rule, auto‑finish).
- 🎙️ **Real‑time audio analysis** – measures breath effort, duration, and stability.
- 🗣️ **Cloud‑ready voice prompts** – uses `gTTS` for cross‑platform compatibility.
- 📊 **Interactive Plotly chart** – fixed 0–100 Y‑axis, colour‑coded bars (Practice 🟠 / Live 🟣), passing line at 80%.
- 📈 **Attempt history & trends** – summary card + numbered trend list with UP/DOWN/SAME arrows.
- 🔄 **Session controls** – reset Live session or clear all history.
- ☁️ **Dockerised & deployed** – runs on AWS EC2.
- 📱 **PWA installable** – works offline after first load on supported devices.

---

## 🛠️ Tech Stack

| Category       | Technologies                      |
| :------------- | :-------------------------------- |
| **Frontend/UI**| Gradio 5.0                        |
| **Audio**      | SciPy, NumPy                      |
| **TTS**        | gTTS (Google Text‑to‑Speech)      |
| **Charts**     | Plotly, Pandas                    |
| **Backend**    | Pure Python                       |
| **Deployment** | Docker, AWS ECR, AWS EC2          |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- A working microphone

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yujass-DAlab/PFT-AI-Companion.git
cd PFT-AI-Companion

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python spirometry_v4_pwa.py
Open your browser at http://127.0.0.1:7864

🐳 Run with Docker
bash
docker build -t spirometry-pwa .
docker run -d -p 7864:7863 --name spirometry-app -e PYTHONUNBUFFERED=1 spirometry-pwa
☁️ AWS Deployment
Live URL: http://18.225.32.182:7864

The app is containerised and deployed on AWS EC2 using Amazon ECR. See the Dockerfile for details.

📁 Project Structure
text
PFT-AI-Companion/
├── spirometry_v4_pwa.py   # Main application (single file)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container build instructions
├── .dockerignore          # Files to exclude from Docker
└── README.md              # This file

👩‍⚕️ User Flow
Choose Practice or Live – coaching voice starts automatically.

Click Record (start/stop toggle) – blow when you hear "BLAST out!".

Score appears instantly – gauge, chart, and summary update.

In Live mode, the app tracks attempts and auto‑finishes after 3 passing blows (≥80%) or 8 total attempts.

🧠 Version History
Version	Focus	                  Key Changes
V1	      Single‑page prototype	Basic audio + pyttsx3 (Windows only).
V2	      Modular architecture	   Split UI (pages/) and logic (utils/). Added Live mode and therapist.
V3	      Unified single page	   Removed pages/ and utils/; switched to gTTS; added Plotly charts; AWS deployment.
V4	      PWA + latency fix	      Fixed mode‑switch latency, improved UI, added PWA manifest + service worker.

⚠️ Limitations
Microphone requires HTTPS – on public IPs, the mic will not work over HTTP. All other features work fine.

Surrogate metrics – measures amplitude/duration, not calibrated flow/volume (FEV₁, FVC).

No clinical validation – this is a coaching tool, not a diagnostic device.

Internet required – gTTS needs an active connection to generate voice prompts.

🔮 Future Plans (V5+)
HTTPS + SSL – add a Let's Encrypt certificate for full microphone support on AWS.

Real‑time flow‑volume loop – visualize your breath as you blow.

Session history storage – save attempts to a database and generate PDF reports.

Multi‑language support – Spanish, Mandarin, etc.

🙏 Acknowledgments
This project was developed with technical guidance from AI language models (ChatGPT, DeepSeek) and the open‑source community:

Gradio – web UI framework

gTTS – cloud‑based Text‑to‑Speech

Plotly – interactive charts

SciPy & NumPy – audio signal processing

📄 License
MIT License – see the LICENSE file for details.

Built with ❤️ for patient empowerment in respiratory health.

Screenshots
Unified Interface (V4)
The new single-page layout puts everything – Practice/Live modes, scoring, and history – on one screen.
<img width="731" height="923" alt="v4_final" src="https://github.com/user-attachments/assets/9f1ede8e-d050-40c1-a676-f3fe4fcd8be7" />



AWS Deployment
The app is containerized with Docker and deployed on AWS EC2.
<img width="688" height="920" alt="URL18 225 32 182 7864" src="https://github.com/user-attachments/assets/a48cdcab-5ed4-4310-bdb7-20f828de0b34" />

 ```
