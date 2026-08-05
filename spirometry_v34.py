"""
=========================================================
Spirometry V34 – Final Polished Version
Practice & Live AI Companion on One Screen

Author: Jasmine Yu, DeepSeek, ChatGPT
=========================================================
"""
print("🟢 1. Script started...")

import time
import threading
import re
import os
print("🟢 2. Standard imports done...")

try:
    import gradio as gr
    print("🟢 3. Gradio imported.")
except Exception as e:
    print(f"❌ Gradio import failed: {e}")
    exit()

try:
    import numpy as np
    import pandas as pd
    print("🟢 4. Numpy/Pandas imported.")
except Exception as e:
    print(f"❌ Numpy/Pandas import failed: {e}")
    exit()

try:
    import pyttsx3
    print("🟢 5. pyttsx3 imported.")
except Exception as e:
    print(f"❌ pyttsx3 import failed: {e}")
    exit()

try:
    from scipy.io import wavfile
    from scipy.signal import hilbert
    print("🟢 6. Scipy imported successfully.")
except Exception as e:
    print(f"❌ Scipy import failed: {e}")
    print("   Please run: pip install scipy")
    exit()

print("🟢 7. All imports successful. Building UI...")

# --------------------------------------------------
# TTS (Thread-Safe, FAST)
# --------------------------------------------------

_lock = threading.Lock()

def speak(text):
    if not text:
        return
    with _lock:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 300)
            time.sleep(0.05)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"⚠️ TTS error: {e}")

# --------------------------------------------------
# TUNED V3 AUDIO ENGINE
# --------------------------------------------------

class AudioEngine:
    @staticmethod
    def extract_features(filepath):
        if filepath is None:
            return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}

        try:
            sr, data = wavfile.read(filepath)
            if data.ndim > 1:
                data = np.mean(data, axis=1)
            data = data.astype(np.float32)
            if np.max(np.abs(data)) > 0:
                data /= np.max(np.abs(data))

            data = data - np.mean(data)
            if np.max(np.abs(data)) > 0:
                data = data / np.max(np.abs(data))

            envelope = np.abs(hilbert(data))
            duration = len(data) / sr

            threshold = 0.02
            onset_candidates = np.where(envelope > threshold)[0]
            if len(onset_candidates) > 0:
                onset = onset_candidates[0]
                onset = max(0, onset - int(0.05 * sr))
            else:
                onset = 0

            window_samples = int(0.4 * sr)
            explosion_window = envelope[onset:onset + window_samples]
            explosion = np.clip(np.max(explosion_window), 0, 1) if len(explosion_window) > 0 else 0

            stab_start = onset + int(0.5 * sr)
            stab_end = onset + int(6.0 * sr)
            stab_end = min(stab_end, len(envelope))
            sustain = envelope[stab_start:stab_end]

            if len(sustain) > 20:
                mean = np.mean(sustain)
                std = np.std(sustain)
                cv = std / (mean + 1e-6)
                stability = np.clip(1 - cv, 0, 1)
            else:
                stability = 0

            print("--------------------------------")
            print(f"Onset Time       : {onset / sr:.2f}s")
            print(f"Explosion (tuned): {explosion:.3f}")
            print(f"Duration         : {duration:.2f}s")
            print(f"Stability (tuned): {stability:.3f}")
            print("--------------------------------")

            return {
                "explosion": round(float(explosion), 3),
                "duration": round(float(duration), 2),
                "stability": round(float(stability), 3)
            }
        except Exception as e:
            print(f"❌ AudioEngine error: {e}")
            return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

MIN_DURATION = 6.0
MIN_EXPLOSION = 0.30
MIN_STABILITY = 0.70
MAX_ATTEMPTS = 8

# --------------------------------------------------
# COACHING SEQUENCE
# --------------------------------------------------

COACH_SEQUENCE = [
    (1.0, "🧘 Relax", "Relax."),
    (1.0, "Get Ready", "Get ready."),
    (1.0, "Take a deep breath in", "Take a deep breath in."),
    (1.0, "3", "Three. Deeper"),
    (1.0, "2", "Two. Deeper"),
    (1.0, "1", "One. Deeper. Click Record now!"),
    (1.0, "💨 BLAST out!", "Blast out fast and hard!"),
    (1.0, "Keep Going", "Keep going."),
    (1.0, "Keep Going", "Keep going."),
    (1.0, "Keep Going", "Keep going."),
    (1.0, "Don't Stop", "Don't stop."),
    (1.0, "Almost There", "Almost there."),
    (1.0, "Finish", "Finish."),
]

# --------------------------------------------------
# AUDIO ANALYSIS
# --------------------------------------------------

def analyze_audio(audio_filepath):
    if audio_filepath is None or not os.path.exists(audio_filepath):
        return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}
    return AudioEngine.extract_features(audio_filepath)

def evaluate_attempt(features):
    blast = min(features["explosion"] / MIN_EXPLOSION, 1.0) * 100
    duration = min(features["duration"] / MIN_DURATION, 1.0) * 100
    stability = min(features["stability"] / MIN_STABILITY, 1.0) * 100
    total = round(blast * 0.50 + duration * 0.30 + stability * 0.20)

    weakest = min(blast, duration, stability)
    if weakest == blast:
        if blast < 80:
            specific_advice = "🔹 Your **Explosive Start** needs work. Try a sudden, sharp cough-like burst at the very beginning."
        else:
            specific_advice = "✅ Your **Explosive Start** is strong! Maintain that sharp burst."
    elif weakest == duration:
        if duration < 80:
            specific_advice = "🔹 Your **Duration** needs work. Focus on exhaling steadily for at least 6 seconds."
        else:
            specific_advice = "✅ Your **Duration** is solid! Keep holding that steady flow."
    else:
        if stability < 80:
            specific_advice = "🔹 Your **Consistency** is dropping. Keep your airflow steady throughout the entire blow—imagine steady candle pressure."
        else:
            specific_advice = "✅ Your **Consistency** is excellent! Your flow is nice and steady."

    if total >= 95:
        stars = "⭐⭐⭐⭐⭐"
        base_advice = "Outstanding maneuver!"
    elif total >= 90:
        stars = "⭐⭐⭐⭐"
        base_advice = "Excellent blast!"
    elif total >= 80:
        stars = "⭐⭐⭐"
        base_advice = "Good effort!"
    else:
        stars = "⭐⭐"
        base_advice = "Keep practicing. Focus on your weakest area above."

    pass_fail = f"**Pass/Fail:** Blast {'✅' if blast>=80 else '⏳'} | Duration {'✅' if duration>=80 else '⏳'} | Stability {'✅' if stability>=80 else '⏳'}"

    report = f"""
### Performance

Explosive Start : **{blast:.0f}%**

Duration : **{duration:.0f}%**

Consistency : **{stability:.0f}%**

---

## {stars}

{base_advice}

{specific_advice}

{pass_fail}

Overall Score:

# **{total}%**
"""
    return report, total, blast, duration, stability

# --------------------------------------------------
# UNIFIED ATTEMPT HISTORY
# --------------------------------------------------

attempt_history = []  # Global list of (score, mode, blast, duration, stability)

def log_attempt(score, mode, blast, duration, stability):
    attempt_history.append((score, mode, blast, duration, stability))

def clear_all_history():
    """Completely resets attempt_history and live_session."""
    global attempt_history, live_session
    attempt_history = []
    live_session = {"total_attempts": 0, "attempts": []}

def get_unified_chart():
    if not attempt_history:
        return pd.DataFrame(columns=["Attempt", "Score"])
    scores = [s[0] for s in attempt_history]
    modes = [s[1] for s in attempt_history]
    labels = [f"{i+1} ({'P' if m=='practice' else 'L'})" for i, m in enumerate(modes)]
    return pd.DataFrame({"Attempt": labels, "Score": scores})

def get_attempt_summary():
    if not attempt_history:
        return "No attempts recorded yet."
    total = len(attempt_history)
    practice_count = sum(1 for s, m, b, d, st in attempt_history if m == "practice")
    live_count = total - practice_count
    passing = sum(1 for s, m, b, d, st in attempt_history if s >= 80)
    failing = total - passing
    return f"""
**Attempt Summary:**  
- **Total Blows:** {total}  
- **Practice:** {practice_count} | **Live:** {live_count}  
- **Passing (≥80%):** {passing} | **Failing (<80%):** {failing}
    """

def get_detailed_summary():
    if not attempt_history:
        return "⭐ No attempts yet. Complete a blow to see your detailed summary."
    scores = [s[0] for s in attempt_history]
    blasts = [s[2] for s in attempt_history]
    durations = [s[3] for s in attempt_history]
    stabilities = [s[4] for s in attempt_history]
    avg_score = np.mean(scores)
    avg_blast = np.mean(blasts)
    avg_duration = np.mean(durations)
    avg_stability = np.mean(stabilities)

    if avg_score >= 95:
        stars = "⭐⭐⭐⭐⭐"
        comment = "Outstanding consistency!"
    elif avg_score >= 90:
        stars = "⭐⭐⭐⭐☆"
        comment = "Excellent consistency!"
    elif avg_score >= 80:
        stars = "⭐⭐⭐☆☆"
        comment = "Good consistency. Focus on your weakest area."
    elif avg_score >= 70:
        stars = "⭐⭐☆☆☆"
        comment = "Fair consistency. Keep practicing."
    else:
        stars = "⭐☆☆☆☆"
        comment = "Keep practicing. Each attempt builds coordination."

    if len(scores) >= 2:
        last = scores[-1]
        prev = scores[-2]
        trend = "📈 Improving" if last > prev else ("📉 Declining" if last < prev else "➡️ Stable")
    else:
        trend = "⏳ Not enough data"

    return f"""
### 📊 Detailed Summary

**Overall Star Rating:** {stars}  
{comment}

**Averages:**  
- Explosive Start: **{avg_blast:.1f}%**  
- Duration: **{avg_duration:.1f}%**  
- Consistency: **{avg_stability:.1f}%**  

**Trend:** {trend}
"""

def get_trend_list():
    if not attempt_history:
        return "No attempts yet."
    lines = []
    for i, (score, mode, blast, dur, stab) in enumerate(attempt_history, 1):
        if i == 1:
            arrow = "➡️"
        else:
            prev_score = attempt_history[i-2][0]
            arrow = "🔼" if score > prev_score else ("🔽" if score < prev_score else "➡️")
        mode_emoji = "🟠" if mode == "practice" else "🟣"
        lines.append(f"{i}. {mode_emoji} **{score}%** {arrow}")
    return "\n".join(lines)

# --------------------------------------------------
# STREAMING FUNCTIONS
# --------------------------------------------------

def stream_practice():
    status = "🟠 **Practice Mode**"
    coach_text = f"{status}\n\n### 🎧 Listen to the coach...\n\n"
    coach_text += "*Click the Record button when you hear 'One' to start capturing your blow.*\n\n---\n\n"
    for delay, sentence, tts_text in COACH_SEQUENCE:
        coach_text += f"**{sentence}**\n\n"
        speak(tts_text)
        yield "practice", status, coach_text
        time.sleep(delay)
    coach_text += "\n---\n✅ **Coaching finished. Click Record to capture your blow!**"
    yield "practice", status, coach_text

def stream_live():
    status = "🟣 **Live Mode**"
    coach_text = f"{status}\n\n### 🎧 Listen to the coach...\n\n"
    coach_text += "*Click the Record button when you hear 'One' to start capturing your blow.*\n\n---\n\n"
    for delay, sentence, tts_text in COACH_SEQUENCE:
        coach_text += f"**{sentence}**\n\n"
        speak(tts_text)
        yield "live", status, coach_text
        time.sleep(delay)
    coach_text += "\n---\n✅ **Coaching finished. Click Record to capture your blow!**"
    yield "live", status, coach_text

# --------------------------------------------------
# LIVE SESSION STATE (used for 3/8 rule)
# --------------------------------------------------

live_session = {"total_attempts": 0, "attempts": []}

def analyze_recording(audio_filepath, current_mode, status_text):
    global attempt_history, live_session
    if audio_filepath is None or not os.path.exists(audio_filepath):
        return (
            "⚠️ No recording detected. Click Record and try again.",
            0,
            gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
            get_attempt_summary(),
            "**Attempts:** 0 / 8",
            gr.update(visible=False),
            gr.update(),
            "No attempts yet.",
            "No attempts yet.",
            "0%"
        )
    try:
        features = analyze_audio(audio_filepath)
        report, score, blast, duration, stability = evaluate_attempt(features)
    except Exception as e:
        return (
            f"❌ Error analyzing audio: {str(e)}. Please try again.",
            0,
            gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
            get_attempt_summary(),
            "**Attempts:** 0 / 8",
            gr.update(visible=False),
            gr.update(),
            "No attempts yet.",
            "No attempts yet.",
            "0%"
        )
    log_attempt(score, current_mode, blast, duration, stability)
    if current_mode == "live":
        live_session["total_attempts"] += 1
        live_session["attempts"].append(score)
        total = live_session["total_attempts"]
        counter_text = f"**Attempts:** {total} / {MAX_ATTEMPTS}"
        if total >= MAX_ATTEMPTS:
            report += "\n\n⛔ **Maximum attempts reached.** Press 'Reset Live Session' to start over."
            reset_visible = gr.update(visible=True)
        else:
            reset_visible = gr.update(visible=False)
    else:
        practice_count = sum(1 for s, m, b, d, st in attempt_history if m == "practice")
        counter_text = f"**Practice Attempts:** {practice_count}"
        reset_visible = gr.update(visible=False)

    chart_data = get_unified_chart()
    summary_text = get_attempt_summary()
    detailed_summary = get_detailed_summary()
    trend_list = get_trend_list()
    current_score_display = f"**{score}%**"

    return (
        report,
        score,
        gr.update(value=chart_data),
        summary_text,
        counter_text,
        reset_visible,
        gr.update(),
        detailed_summary,
        trend_list,
        current_score_display
    )

# --------------------------------------------------
# CLEAR MIC
# --------------------------------------------------

def clear_mic():
    return gr.update(value=None)

# --------------------------------------------------
# RESET LIVE (only resets live_session, keeps attempt_history)
# --------------------------------------------------

def reset_live():
    global live_session
    live_session = {"total_attempts": 0, "attempts": []}
    return (
        "🔄 Live session reset. Click 'Live AI Companion' to start again.",
        0,
        gr.update(value=get_unified_chart()),
        get_attempt_summary(),
        "**Attempts:** 0 / 8",
        gr.update(visible=False),
        gr.update(),
        get_detailed_summary(),
        get_trend_list(),
        "0%"
    )

# --------------------------------------------------
# CLEAR ALL HISTORY (new function)
# --------------------------------------------------

def clear_all_history():
    global attempt_history, live_session
    attempt_history = []
    live_session = {"total_attempts": 0, "attempts": []}
    return (
        "🗑️ All history cleared.",
        0,
        gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
        "No attempts recorded yet.",
        "**Attempts:** 0 / 8",
        gr.update(visible=False),
        gr.update(),
        "⭐ No attempts yet. Complete a blow to see your detailed summary.",
        "No attempts yet.",
        "0%"
    )

# --------------------------------------------------
# THERAPIST & FINISH
# --------------------------------------------------

def request_therapist():
    speak("A respiratory therapist has been notified. Someone will be assisting you shortly.")
    return """
# 👨‍⚕️ Respiratory Therapist Requested

Your respiratory therapist has now been requested. Someone will be assisting you shortly.

The AI Companion will remain available for
education and encouragement, while the
therapist directs the maneuver.

Please follow your therapist's instructions.
"""

def finish_session():
    speak("Session complete. Excellent effort.")
    return """
# 🎉 Session Complete

Excellent effort today.

Remember:

Every maneuver trains your muscles and lungs to coordinate better with the test.

Thank you for practicing with
AI Spirometry Companion.
"""

# --------------------------------------------------
# BUILD UI
# --------------------------------------------------

def build_spirometry():
    gr.HTML("""
    <style>
        .main-title { font-size: 48px !important; font-weight: bold !important; text-align: center !important; }
        /* Animated lung emoji */
        @keyframes breathe {
            0% { transform: scale(1); }
            50% { transform: scale(1.15); }
            100% { transform: scale(1); }
        }
        .lung-emoji {
            display: inline-block;
            animation: breathe 2.5s ease-in-out infinite;
        }
        .big-score { font-size: 72px !important; font-weight: bold !important; text-align: center !important; color: #2c3e50; }
        #therapist-btn { background-color: #3498db !important; color: white !important; border: 2px solid #2980b9 !important; font-weight: bold !important; }
        #therapist-btn:hover { background-color: #5dade2 !important; }
        #practice-btn { background-color: #f39c12 !important; color: white !important; border: 2px solid #d68910 !important; font-weight: bold !important; }
        #practice-btn:hover { background-color: #f5b041 !important; }
        #live-btn { background-color: #8e44ad !important; color: white !important; border: 2px solid #6c3483 !important; font-weight: bold !important; }
        #live-btn:hover { background-color: #a569bd !important; }
        #finish-btn { background-color: #1abc9c !important; color: white !important; border: 2px solid #16a085 !important; font-weight: bold !important; }
        #finish-btn:hover { background-color: #48c9b0 !important; }
        #reset-btn { background-color: #f1c40f !important; color: black !important; border: 2px solid #d4ac0d !important; font-weight: bold !important; }
        #reset-btn:hover { background-color: #f4d03f !important; }
        #clear-btn { background-color: #e74c3c !important; color: white !important; border: 2px solid #c0392b !important; font-weight: bold !important; }
        #clear-btn:hover { background-color: #c0392b !important; }
        #clear-history-btn { background-color: #e67e22 !important; color: white !important; border: 2px solid #d35400 !important; font-weight: bold !important; }
        #clear-history-btn:hover { background-color: #d35400 !important; }
        .audio-wrap .wrap { height: auto !important; min-height: 120px !important; }
        .audio-wrap .record-button { height: 80px !important; font-size: 24px !important; }
        /* Bigger status tag (circle) */
        .status-tag { font-size: 32px !important; font-weight: bold !important; padding: 10px !important; border-radius: 12px !important; text-align: center !important; }
        /* Uniform section headers: slightly smaller than buttons */
        .section-header {
            font-size: 22px !important;
            font-weight: 600 !important;
            margin-top: 16px !important;
            margin-bottom: 8px !important;
            color: #2c3e50 !important;
        }

        /* About Accordion styling */
        .about-accordion {
            margin: 12px 0 !important;
        }
        .about-accordion .accordion {
            border: none !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            margin-bottom: 10px !important;
            background: white !important;
        }
        .about-accordion .accordion .accordion-header {
            background: #f8f9fa !important;
            padding: 14px 20px !important;
            font-weight: 600 !important;
            font-size: 18px !important;
            border-radius: 12px !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            border-left: 6px solid #3498db !important;
        }
        .about-accordion .accordion .accordion-header:hover {
            background: #e9ecef !important;
            transform: translateX(4px) !important;
        }
        .about-accordion .accordion .accordion-content {
            padding: 16px 20px !important;
            background: white !important;
            border-top: 1px solid #e9ecef !important;
            color: #1a1a1a !important;
        }
        .about-accordion .accordion .accordion-content h1, 
        .about-accordion .accordion .accordion-content h2 { color: #2c3e50 !important; }
        .about-accordion .accordion .accordion-content p, 
        .about-accordion .accordion .accordion-content li { color: #1a1a1a !important; }
        /* Different border colors for each card */
        .card-bg .accordion-header { border-left-color: #2c3e50 !important; }
        .card-fev1 .accordion-header { border-left-color: #e74c3c !important; }
        .card-dlco .accordion-header { border-left-color: #8e44ad !important; }
        .card-fvc .accordion-header { border-left-color: #e67e22 !important; }
        .card-ratio .accordion-header { border-left-color: #1abc9c !important; }
        .card-pft .accordion-header { border-left-color: #2ecc71 !important; }
        .card-tips .accordion-header { border-left-color: #f39c12 !important; }
    </style>
    """)

    with gr.Column():
        # --- TITLE with animated lung ---
        gr.Markdown("""
        <div class="main-title">
            <span class="lung-emoji">🫁</span> AI Spirometry Companion (V34)
        </div>
        **One page. Two modes. All stats.**
        """)

        # --- ABOUT SECTION: Clickable Card Accordions ---
        with gr.Accordion("📖 About This App", open=False, elem_classes="about-accordion"):
            # Background Card
            with gr.Accordion("📘 Background Information", open=False, elem_classes="card-bg"):
                gr.Markdown("""
**Welcome!**

Feeling a little nervous? You're not alone. Not too long ago, I experienced my very first Pulmonary Function Test as well. I quickly discovered that the breathing maneuvers were much more demanding and different from normal breathing than I had expected. Many first-time patients feel exactly the same way. That's one of the reasons this AI Companion was created—to help you become more familiar with the procedure, build confidence, and reduce unnecessary anxiety before and during your examination. We'll take it one step at a time.

Pulmonary Function Testing (PFT) is a **non-invasive physiological test** used to evaluate how well your lungs are functioning. It measures the amount of air your lungs can hold, how quickly you can move air in and out of your lungs, and how efficiently oxygen passes from your lungs into your blood. The test itself provides important information that helps your doctor evaluate your respiratory health.

The entire appointment usually lasts **30–60 minutes**, depending on the number of tests ordered. Because several breathing methods require maximum effort, the test may feel different from your normal breathing. This is completely expected. Most first-time patients require several practice attempts before producing an acceptable result.

**To obtain the most accurate results:**

- Follow the respiratory therapist's coaching or my instructions carefully.
- Wear comfortable clothing that does not restrict breathing.
- Avoid smoking before the test.
- Avoid heavy meals immediately before the procedure.
- Inform the staff if you recently had chest pain, eye surgery, abdominal surgery, very high or very low blood pressure readings, severe dizziness, or if you become uncomfortable at any time during testing.

> **Remember:** You are not expected to perform perfectly on your first attempt. The respiratory therapist is there to coach you throughout the procedure on demand and answer any questions you may have.
                """)

            # FEV₁ Card
            with gr.Accordion("⚡ FEV₁ (Forced Expiratory Volume in 1 Second)", open=False, elem_classes="card-fev1"):
                gr.Markdown("""
**FEV₁** stands for **Forced Expiratory Volume in One Second**. It is the amount of air you can forcefully blow out during the **first second** of a maximal exhalation.

- This is one of the most important numbers in a PFT report.
- A low FEV₁ may indicate obstructive lung disease (like asthma or COPD).
- In a healthy person, FEV₁ is usually around 80% or more of the predicted value for their age, sex, and height.
- The test requires a **sharp, explosive start** – that is why our AI places heavy weight on the "Explosive Start" metric.
                """)

            # DLCO Card
            with gr.Accordion("🌬️ DLCO (Diffusing Capacity)", open=False, elem_classes="card-dlco"):
                gr.Markdown("""
**DLCO** stands for **Diffusing Capacity of the Lung for Carbon Monoxide**. It measures how efficiently gases move from the air sacs of your lungs into your bloodstream.

- The test uses a tiny, safe amount of carbon monoxide to estimate how well oxygen would transfer into your blood.
- A low DLCO may indicate conditions like emphysema, pulmonary fibrosis, or anemia.
- This test is usually done during a full PFT session, but is not part of the basic spirometry we practice here.
                """)

            # FVC Card
            with gr.Accordion("💨 FVC (Forced Vital Capacity)", open=False, elem_classes="card-fvc"):
                gr.Markdown("""
**FVC** stands for **Forced Vital Capacity**. It is the total amount of air you can forcefully exhale after taking the deepest breath possible.

- This measures the *volume* of air your lungs can move.
- A low FVC may indicate restrictive lung disease (like pulmonary fibrosis).
- Our practice focuses on the *timing* and *consistency* of the exhalation, which are key to achieving a good FVC measurement.
                """)

            # FEV₁/FVC Ratio Card
            with gr.Accordion("📊 FEV₁ / FVC Ratio", open=False, elem_classes="card-ratio"):
                gr.Markdown("""
**FEV₁ / FVC Ratio** is a comparison between the amount of air you blow out in the first second (FEV₁) and the total amount you blow out (FVC).

- This ratio helps doctors determine whether a breathing problem is **obstructive** (low ratio) or **restrictive** (normal or high ratio).
- A normal ratio is usually > 70–80%.
- This is a key diagnostic indicator used by pulmonologists.
                """)

            # PFT Card
            with gr.Accordion("🫁 PFT (Pulmonary Function Test)", open=False, elem_classes="card-pft"):
                gr.Markdown("""
**PFT** stands for **Pulmonary Function Test**. It is a group of non-invasive tests that evaluate how well your lungs are working.

- PFTs measure lung volume, capacity, flow rates, and gas exchange.
- They are used to diagnose conditions like asthma, COPD, pulmonary fibrosis, and to monitor treatment effectiveness.
- This app focuses on **spirometry** – the most common part of a PFT, which measures how much and how quickly you can move air.
                """)

            # Before We Begin Card
            with gr.Accordion("⭐ Before We Begin", open=False, elem_classes="card-tips"):
                gr.Markdown("""
- ✔ Listen carefully to your respiratory therapist or my instructions.
- ✔ Take your time between attempts.
- ✔ If you become dizzy, uncomfortable, or need a break, please tell the staff immediately.
- ✔ Multiple attempts are normal.
- ✔ The goal is **not perfection**. The goal is obtaining reliable measurements.
                """)

        # --- MODE STATUS (Bigger circle) ---
        mode_status = gr.Markdown(value="🟠 **Practice Mode**", elem_classes="status-tag")

        # --- THERAPIST BUTTON ---
        with gr.Row():
            therapist_btn = gr.Button("👨‍⚕️ Request Respiratory Therapist", scale=2, elem_id="therapist-btn")
        therapist_box = gr.Markdown()

        # --- RECORD + CLEAR MIC ---
        with gr.Row():
            mic_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Click RECORD when you hear 'One' (click STOP to score)",
                format="wav",
                scale=3,
                elem_classes="audio-wrap"
            )
            clear_btn = gr.Button("✖ Clear Audio", scale=1, elem_id="clear-btn")

        # --- MODE BUTTONS ---
        with gr.Row():
            practice_btn = gr.Button("🟠 Practice Mode", scale=2, elem_id="practice-btn")
            live_btn = gr.Button("🟣 Live AI Companion", scale=2, elem_id="live-btn")

        # --- INSTANT EFFORT SCORE (section header) ---
        gr.Markdown("### 📊 Instant Effort Score", elem_classes="section-header")
        with gr.Row():
            big_score_display = gr.Markdown(value="**0%**", elem_classes="big-score")
        score_slider = gr.Slider(label="Overall Score (%)", minimum=0, maximum=100, step=1, value=0, interactive=False, scale=3)

        # --- UNIFIED ATTEMPT PROGRESS (section header) ---
        gr.Markdown("### 📈 Unified Attempt Progress (Practice + Live)", elem_classes="section-header")
        attempt_summary = gr.Markdown(value="No attempts recorded yet.")
        attempt_chart = gr.BarPlot(
            value=pd.DataFrame(columns=["Attempt", "Score"]),
            x="Attempt",
            y="Score",
            title="All Attempts (P=Practice, L=Live)",
            height=300
        )

        # --- DETAILED SUMMARY & TREND (section header) ---
        gr.Markdown("### 📊 Detailed Summary & Trend", elem_classes="section-header")
        with gr.Row():
            detailed_summary_box = gr.Markdown(value="No attempts yet.", scale=1)
            trend_list_box = gr.Markdown(value="No attempts yet.", scale=1)

        # --- LIVE SESSION TRACKER ---
        gr.Markdown("---")
        gr.Markdown("### 📊 Live Session Tracker", elem_classes="section-header")
        attempt_counter = gr.Markdown(value="**Attempts:** 0 / 8")
        with gr.Row():
            reset_btn = gr.Button("🔄 Reset Live Session", visible=False, elem_id="reset-btn")
            clear_history_btn = gr.Button("🗑️ Clear All History", visible=True, elem_id="clear-history-btn")

        # --- FINISH SESSION (removed "Session Controls" heading) ---
        gr.Markdown("---")
        with gr.Row():
            finish_btn = gr.Button("🔷 Finish Session", scale=2, elem_id="finish-btn")
        finish_box = gr.Markdown()

        # --- COACHING & RESULTS ---
        gr.Markdown("---")
        gr.Markdown("### 📝 Coaching & Results", elem_classes="section-header")
        coach_box = gr.Markdown(value="", height=350)

        gr.Markdown("---")
        gr.Markdown("⚠️ **Disclaimer:** Educational purposes only. Not a substitute for professional clinical judgment.")

    # -----------------------------------------
    # EVENTS
    # -----------------------------------------

    current_mode = gr.State("practice")

    therapist_btn.click(fn=request_therapist, outputs=therapist_box)
    finish_btn.click(fn=finish_session, outputs=finish_box)

    practice_btn.click(
        fn=stream_practice,
        inputs=[],
        outputs=[current_mode, mode_status, coach_box]
    )
    live_btn.click(
        fn=stream_live,
        inputs=[],
        outputs=[current_mode, mode_status, coach_box]
    )

    mic_input.change(
        fn=analyze_recording,
        inputs=[mic_input, current_mode, mode_status],
        outputs=[
            coach_box,
            score_slider,
            attempt_chart,
            attempt_summary,
            attempt_counter,
            reset_btn,
            mic_input,
            detailed_summary_box,
            trend_list_box,
            big_score_display
        ]
    )

    clear_btn.click(
        fn=clear_mic,
        inputs=[],
        outputs=[mic_input]
    )

    reset_btn.click(
        fn=reset_live,
        inputs=[],
        outputs=[
            coach_box,
            score_slider,
            attempt_chart,
            attempt_summary,
            attempt_counter,
            reset_btn,
            mic_input,
            detailed_summary_box,
            trend_list_box,
            big_score_display
        ]
    )

    clear_history_btn.click(
        fn=clear_all_history,
        inputs=[],
        outputs=[
            coach_box,
            score_slider,
            attempt_chart,
            attempt_summary,
            attempt_counter,
            reset_btn,
            mic_input,
            detailed_summary_box,
            trend_list_box,
            big_score_display
        ]
    )

    return None

# --------------------------------------------------
# LAUNCH
# --------------------------------------------------
if __name__ == "__main__":
    print("🟢 8. Entering main block...")
    with gr.Blocks(title="PFT AI Companion V34") as demo:
        print("🟢 9. Building UI...")
        build_spirometry()
    print("🟢 10. UI built, launching now...")
    demo.launch(server_name="0.0.0.0", server_port=7863)
    print("🟢 11. Server should be running.")