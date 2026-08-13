# AI Spirometry Companion (V4 – PWA Edition)

**One page. Two modes. All stats.**

A Progressive Web App for practicing Pulmonary Function Tests (PFT) with AI coaching, real-time scoring, and Practice/Live modes.

---

## 🚀 Live Demo

👉 [Live Demo](http://18.225.32.182:7864)

> ⚠️ **Deployment note:** The current AWS deployment uses HTTP on a public EC2 IP address. Modern browsers require a secure origin (HTTPS) for full microphone and Progressive Web App functionality. Core coaching, scoring, visualization, and educational features remain available, but PWA installation and microphone behavior may vary by browser and device.

---

## 📖 Overview

The **PFT AI Companion V4** is a unified, single-page application designed to help users practice and prepare for spirometry.

It combines **Practice** and **Live Test** modes into one interface, using real-time audio analysis and cloud-based Text-to-Speech (TTS) to guide users through the critical steps of a forced expiratory maneuver:

1. 🌬️ **Breathe In Deeply** – maximize inhalation.
2. 💨 **Blast Out** – perform a forceful, explosive exhalation.
3. ⏱️ **Sustain** – continue blowing for at least 6 seconds.

The application evaluates:

* **Explosive Start (amplitude)**
* **Duration**
* **Airflow Stability**

It then provides immediate coaching feedback and a color-coded performance score with a passing threshold of **80%**.

> ⚠️ **Clinical Disclaimer:** This application is for educational and preparation purposes only. It does not diagnose pulmonary disease, perform clinical spirometry, or replace professional clinical judgment.

---

## ✨ Key Features

* 📘 **Collapsible About section** – background information, FEV₁, DLCO, PFT concepts, and preparation tips.
* 🎮 **Two modes in one page** – Practice mode for unlimited practice and Live mode for structured attempts.
* 🎙️ **Real-time audio analysis** – evaluates breath effort, duration, and stability.
* 🗣️ **Cloud-ready voice prompts** – uses `gTTS` for cross-platform text-to-speech.
* 📊 **Interactive Plotly visualization** – fixed 0–100 Y-axis, color-coded Practice/Live results, and an 80% passing line.
* 📈 **Attempt history and trends** – tracks scores and displays UP/DOWN/SAME trends.
* 🧑‍⚕️ **Respiratory Therapist coaching interface** – provides requested therapist guidance and coaching feedback.
* 🔄 **Session controls** – reset the Live session and clear attempt history.
* ☁️ **Dockerized deployment** – deployed to AWS EC2 using Docker and Amazon ECR.
* 📱 **PWA-ready architecture** – includes PWA manifest/service-worker support, with full installation functionality dependent on secure-origin requirements.

---

## 🛠️ Tech Stack

| Category                   | Technologies                     |
| :------------------------- | :------------------------------- |
| **Frontend / UI**          | Gradio                           |
| **Audio Processing**       | SciPy, NumPy                     |
| **Text-to-Speech**         | gTTS                             |
| **Charts / Visualization** | Plotly, Pandas                   |
| **Backend**                | Python                           |
| **Containerization**       | Docker                           |
| **Cloud Deployment**       | AWS ECR, AWS EC2                 |
| **PWA**                    | Web App Manifest, Service Worker |

---

## 🚀 Run Locally

### Prerequisites

* Python 3.11+
* Working microphone
* Internet connection for gTTS voice generation

### Installation

```bash
# Clone the repository
git clone https://github.com/yujass-DAlab/PFT-AI-Companion.git

# Enter the project directory
cd PFT-AI-Companion

# Install dependencies
pip install -r requirements.txt

# Run the application
python spirometry_v4_pwa.py
```

Open your browser at:

```text
http://127.0.0.1:7864
```

---

## 🐳 Run with Docker

Build the image:

```bash
docker build -t spirometry-pwa .
```

Run the container:

```bash
docker run -d \
  -p 7864:7863 \
  --name spirometry-app \
  -e PYTHONUNBUFFERED=1 \
  spirometry-pwa
```

The application can then be accessed through the mapped port.

---

## ☁️ AWS Deployment

The application is containerized with Docker and deployed on **AWS EC2** using **Amazon ECR**.

### Current deployment

**Live URL:** http://18.225.32.182:7864

The current deployment intentionally uses a public HTTP endpoint rather than HTTPS.

### Current HTTPS limitation

Modern browsers restrict certain capabilities, including microphone access and full PWA installation behavior, when an application is served from an insecure public origin.

As a result:

* The application may appear as a home-screen shortcut rather than a fully featured installed PWA.
* Microphone access may be restricted on some mobile and desktop browsers.
* Rich PWA installation UI may not be available.
* Offline/install behavior may vary by platform.

These are deployment/security-context limitations rather than limitations of the application's core coaching and scoring logic.

### Future deployment improvement

A future version can add:

* HTTPS
* Custom domain
* SSL/TLS certificate
* Full browser microphone support
* Full PWA installation support

---

## 📱 PWA Status

V4 includes the foundation for Progressive Web App functionality, including a web app manifest and service-worker architecture.

However, the current AWS deployment is served over **HTTP**, so browsers may not treat it as a fully installable PWA.

The current implementation should therefore be considered **PWA-ready but not fully production-installed as a PWA on the public AWS endpoint**.

---

## 👩‍⚕️ User Flow

1. **Choose Practice or Live mode** – the application begins the appropriate coaching sequence.
2. **Use the Record control** – start/stop the recording and perform the maneuver when prompted.
3. **Receive immediate feedback** – the application calculates the performance score and updates the gauge, chart, and session history.
4. **Continue practicing or complete the Live session** – Live mode tracks attempts and applies the configured passing/session rules.

---

## 📊 Scoring Concept

The application uses surrogate audio-derived metrics rather than calibrated clinical spirometry measurements.

The performance score considers:

* **Explosive Start** – strength/amplitude of the initial blow.
* **Duration** – ability to sustain the maneuver.
* **Airflow Stability** – consistency of the detected respiratory signal.

An **80% threshold** is used as the application's coaching/pass threshold.

> This score should not be interpreted as a clinical spirometry result or an ATS/ERS diagnostic measurement.

---

## 🧠 Version History

| Version | Focus                         | Key Changes                                                                                                                                          |
| :------ | :---------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| **V1**  | Single-page prototype         | Basic audio analysis and `pyttsx3` voice prompts on Windows.                                                                                         |
| **V2**  | Modular architecture          | Separated UI and logic; added Live mode and therapist functionality.                                                                                 |
| **V3**  | Unified single page           | Removed separate pages/utils structure; switched to gTTS; added Plotly charts and AWS deployment.                                                    |
| **V4**  | PWA + latency/UI improvements | Fixed mode-switch latency, improved audio-prompt behavior, refined UI, added PWA manifest/service-worker support, and improved AWS-ready deployment. |

---

## ⚠️ Limitations

* **HTTPS required for full browser microphone/PWA support** on public deployments.
* **Surrogate metrics:** the application measures audio-derived amplitude, duration, and stability rather than calibrated flow and volume.
* **No clinical validation:** this is an educational coaching tool and not a diagnostic device.
* **No FEV₁/FVC measurement:** the application does not replace clinical spirometry equipment.
* **Internet required for gTTS:** cloud-based voice prompts require an active network connection.
* **Browser/device differences:** microphone and PWA behavior may vary across browsers and operating systems.

---

## 🔮 Future Plans (V5+)

* 🔐 **HTTPS + SSL** – enable secure-origin microphone and full PWA functionality.
* 🌐 **Custom domain** – provide a more professional public deployment.
* 🌬️ **Real-time flow-volume loop** – add more clinically recognizable respiratory visualization.
* 💾 **Session history storage** – persist attempts and generate downloadable reports.
* 📄 **PDF reporting** – generate structured practice/session summaries.
* 🌎 **Multi-language support** – Spanish, Mandarin, and additional languages.
* 📱 **Enhanced mobile experience** – optimize the interface for smaller screens and installed PWA environments.

---

## 🙏 Acknowledgments

This project was developed with technical guidance from AI language models, including **ChatGPT** and **DeepSeek**, together with the open-source software community.

Major technologies used include:

* **Gradio** – web application framework
* **gTTS** – cloud-based Text-to-Speech
* **Plotly** – interactive visualization
* **SciPy** – scientific/audio signal processing
* **NumPy** – numerical computing
* **Pandas** – data processing
* **Docker** – application containerization
* **AWS ECR / EC2** – container registry and cloud deployment

---

## 📄 License

MIT License – see the `LICENSE` file for details.

Built with ❤️ for patient empowerment in respiratory health.

---

## 📸 Screenshots

### Unified Interface (V4)

The new single-page layout puts Practice/Live modes, scoring, coaching, and history into one unified interface.

<img width="731" height="923" alt="V4 Unified Interface" src="https://github.com/user-attachments/assets/d0d1d8cb-4334-4f00-9a17-086892ff4784">

### AWS Deployment

The application is containerized with Docker and deployed on AWS EC2.

<img width="688" height="920" alt="AWS Deployment" src="https://github.com/user-attachments/assets/fd949ab3-0ee3-46c7-88eb-03bd1b7f6ce2">

---

## 🏁 Project Status

**V4 – PWA Edition**

The application is currently deployed on AWS EC2 and demonstrates an end-to-end healthcare AI prototype incorporating:

**Python → Audio Processing → AI-Assisted Coaching → TTS → Interactive Visualization → Docker → AWS**

The current V4 release focuses on demonstrating the complete workflow and a practical patient-facing respiratory coaching experience while clearly identifying the limitations of surrogate respiratory metrics and HTTP-based deployment.
