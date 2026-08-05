# 🫁 PFT AI Companion (V3)

### *Unified Spirometry Coaching & Preparation Tool – Now Live on AWS!*

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-5.0-green.svg)](https://gradio.app/)
[![Plotly](https://img.shields.io/badge/Plotly-6.0-purple.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AWS](https://img.shields.io/badge/Live%20Demo-AWS-orange.svg)](http://3.15.171.219:7863)

---

## 🚀 Live Demo

**Try the V3 app right now:**  
👉 [http://3.15.171.219:7863](http://3.15.171.219:7863)

*Note: The microphone works on `localhost` (HTTPS required for public IPs). All other features – audio coaching, scoring, bar charts – work flawlessly on the cloud.*

---

## 📖 Overview

The **PFT AI Companion V3** is a **unified, single‑page** application that combines Practice and Live test modes into one clean interface. It uses real‑time audio analysis and **cloud‑compatible Text‑to‑Speech (gTTS)** to guide users through the three critical steps of a spirometry maneuver:

1. **🌬️ Breathe In Deeply** – Maximise inhalation.
2. **💨 Blast Out** – Forceful, explosive exhalation.
3. **⏱️ Sustain** – Keep blowing for at least 6 seconds.

The app evaluates **Explosive Start (amplitude)**, **Duration**, and **Airflow Stability**, providing immediate, personalised coaching feedback and a **colour‑coded bar chart** with a passing line at 80%.

**⚠️ Clinical Disclaimer:** This tool is for **educational and preparation purposes only**. It does **not** diagnose lung conditions or replace professional clinical judgment.

---

## ✨ Key Features (V3)

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
- (Optional) Docker for containerised deployment.

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yujass-DAlab/PFT-AI-Companion.git
   cd PFT-AI-Companion