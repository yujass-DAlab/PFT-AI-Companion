"""
=========================================================
Spirometry V33 – Enhanced Summary & Trends
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
import gradio as gr
import numpy as np
import pandas as pd
print("🟢 3. Gradio/Numpy/Pandas done...")
print("🟢 4. pyttsx3 imported...")
from utils.Audio_Engine_v3 import AudioEngine
print("🟢 5. AudioEngine imported...")

# --------------------------------------------------
# TTS (Thread-Safe, FAST)
# --------------------------------------------------

_lock = threading.Lock()

def speak(text):
    if not text:
        return
    with _lock:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 300)
            time.sleep(0.05)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"⚠️ TTS error: {e}")

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

MIN_DURATION = 6.0
MIN_EXPLOSION = 0.60
MIN_STABILITY = 0.70
MAX_ATTEMPTS = 8

# --------------------------------------------------
# COACHING SEQUENCE (YOUR UPDATED VERSION)
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
    else:  # weakest == stability
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
    # Return the raw metrics and total for summary calculations
    return report, total, blast, duration, stability

# --------------------------------------------------
# UNIFIED ATTEMPT HISTORY
# --------------------------------------------------

attempt_history = []  # Each entry: (score, mode, blast, duration, stability)

def log_attempt(score, mode, blast, duration, stability):
    attempt_history.append((score, mode, blast, duration, stability))

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
    """Generates a detailed summary with star rating and breakdown."""
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
    
    # Star rating based on average score
    if avg_score >= 95:
        stars = "⭐⭐⭐⭐⭐"
        comment = "Outstanding consistency! You are ready for the real test."
    elif avg_score >= 90:
        stars = "⭐⭐⭐⭐☆"
        comment = "Excellent consistency! Keep up the great work."
    elif avg_score >= 80:
        stars = "⭐⭐⭐☆☆"
        comment = "Good consistency. Focus on your weakest area to improve further."
    elif avg_score >= 70:
        stars = "⭐⭐☆☆☆"
        comment = "Fair consistency. Keep practicing to build muscle memory."
    else:
        stars = "⭐☆☆☆☆"
        comment = "Keep practicing. Each attempt builds coordination."
    
    # Determine overall trend
    if len(scores) >= 2:
        last = scores[-1]
        prev = scores[-2]
        if last > prev:
            trend = "📈 Improving"
        elif last < prev:
            trend = "📉 Declining"
        else:
            trend = "➡️ Stable"
    else:
        trend = "⏳ Not enough data"
    
    summary = f"""
### 📊 Detailed Summary

**Overall Star Rating:** {stars}  
{comment}

**Averages:**  
- Explosive Start: **{avg_blast:.1f}%**  
- Duration: **{avg_duration:.1f}%**  
- Consistency: **{avg_stability:.1f}%**  

**Trend:** {trend}
"""
    return summary

def get_trend_list():
    """Returns a formatted list of each attempt with a trend arrow."""
    if not attempt_history:
        return "No attempts yet."
    
    lines = []
    for i, (score, mode, blast, dur, stab) in enumerate(attempt_history, 1):
        # Determine arrow and color based on previous score
        if i == 1:
            arrow = "➡️"
        else:
            prev_score = attempt_history[i-2][0]
            if score > prev_score:
                arrow = "🔼"
            elif score < prev_score:
                arrow = "🔽"
            else:
                arrow = "➡️"
        
        # Emoji for mode
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
# LIVE SESSION STATE
# --------------------------------------------------

live_session = {
    "total_attempts": 0,
    "attempts": []
}

def analyze_recording(audio_filepath, current_mode, status_text):
    """
    Triggered when user stops recording. Returns 10 outputs now.
    Added: detailed_summary, trend_list, current_score_display.
    """
    global attempt_history, live_session

    if audio_filepath is None or not os.path.exists(audio_filepath):
        return (
            "⚠️ No recording detected. Click Record and try again.",
            0,
            gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
            get_attempt_summary(),
            "**Attempts:** 0 / 8",
            gr.update(visible=False),
            gr.update(),  # mic placeholder
            "No attempts yet.",
            "No attempts yet.",
            "0%"  # big score display
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

    # Log to UNIFIED history with full metrics
    log_attempt(score, current_mode, blast, duration, stability)
    
    # Update Live session if in Live mode
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

    # Build unified chart & summary
    chart_data = get_unified_chart()
    summary_text = get_attempt_summary()
    detailed_summary = get_detailed_summary()
    trend_list = get_trend_list()
    current_score_display = f"**{score}%**"  # big, bold

    return (
        report,
        score,
        gr.update(value=chart_data),
        summary_text,
        counter_text,
        reset_visible,
        gr.update(),  # mic placeholder
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
# RESET LIVE
# --------------------------------------------------

def reset_live():
    global live_session, attempt_history
    live_session = {"total_attempts": 0, "attempts": []}
    # Do NOT clear attempt_history – we want cumulative stats
    return (
        "🔄 Live session reset. Click 'Live AI Companion' to start again.",
        0,
        gr.update(value=get_unified_chart()),
        get_attempt_summary(),
        "**Attempts:** 0 / 8",
        gr.update(visible=False),
        gr.update(),
        "No attempts yet.",
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
        /* Title large */
        .main-title { font-size: 48px !important; font-weight: bold !important; text-align: center !important; }
        /* Big score display */
        .big-score { font-size: 72px !important; font-weight: bold !important; text-align: center !important; color: #2c3e50; }
        /* Trend arrows color */
        .trend-up { color: #2ecc71; }
        .trend-down { color: #e74c3c; }
        .trend-same { color: #95a5a6; }
        /* Buttons */
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
        .audio-wrap .wrap { height: auto !important; min-height: 120px !important; }
        .audio-wrap .record-button { height: 80px !important; font-size: 24px !important; }
        .status-tag { font-size: 24px !important; font-weight: bold !important; padding: 10px !important; border-radius: 12px !important; text-align: center !important; }

        /* --- FORCE INFO BOX TO BE WHITE BACKGROUND WITH BLACK TEXT (readable in dark mode) --- */
        .info-box {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #2c3e50 !important;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        /* Make every single element inside the info box have black text */
        .info-box * {
            color: #000000 !important;
        }

        /* --- ABOUT BUTTON – BRIGHT YELLOW WITH BLACK TEXT (readable in dark mode) --- */
        #about-btn {
            background-color: #f1c40f !important;
            color: #000000 !important;
            border: 3px solid #d4ac0d !important;
            font-weight: 900 !important;
            font-size: 20px !important;
            padding: 14px 28px !important;
            border-radius: 14px !important;
            min-width: 240px !important;
            white-space: nowrap !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        }
        /* Force button text to be black */
        #about-btn .label, #about-btn span, #about-btn p {
            color: #000000 !important;
        }
        #about-btn:hover {
            background-color: #f39c12 !important;
            transform: scale(1.03) !important;
        }
    </style>
    """)

    with gr.Column():
        # --- TITLE (Large) ---
        gr.Markdown("""
        <div class="main-title">🫁 AI Spirometry Companion (V33)</div>
        **One page. Two modes. All stats.**
        """)

        # --- About Button + Toggle Info ---
        with gr.Row():
            about_btn = gr.Button("📖 About This App", variant="secondary", scale=1, elem_id="about-btn")
        about_box = gr.Markdown(
            value="",
            visible=False,
            elem_classes="info-box"
        )
        # --- YOUR INTEGRATED BACKGROUND AND PROCLAMATION TEXT ---
        about_content = """
# 📘 Background Information

## Welcome!

Feeling a little nervous? You're not alone. Not too long ago, I experienced my very first Pulmonary Function Test as well. I quickly discovered that the breathing maneuvers were much more demanding and different from normal breathing than I had expected. Many first-time patients feel exactly the same way. That's one of the reasons this AI Companion was created—to help you become more familiar with the procedure, build confidence, and reduce unnecessary anxiety before and during your examination. We'll take it one step at a time.

Pulmonary Function Testing (PFT) is a **non-invasive physiological test** used to evaluate how well your lungs are functioning. It measures the amount of air your lungs can hold, how quickly you can move air in and out of your lungs, and how efficiently oxygen passes from your lungs into your blood. The test itself **does not diagnose a disease**; instead, it provides important information that helps your doctor evaluate your respiratory health.

The entire appointment usually lasts **30–60 minutes**, depending on the number of tests ordered. Because several breathing methods require maximum effort, the test may feel different from your normal breathing. This is completely expected. Most first-time patients require several practice attempts before producing an acceptable result.

To obtain the most accurate results:

• Follow the respiratory therapist's coaching or my instructions carefully.

• Wear comfortable clothing that does not restrict breathing.

• Avoid smoking before the test.

• Avoid heavy meals immediately before the procedure.

• Inform the staff if you recently had chest pain, eye surgery, abdominal surgery, very high or very low blood pressure readings, severe dizziness, or if you become uncomfortable at any time during testing.

Remember:

**You are not expected to perform perfectly on your first attempt.**

The respiratory therapist is there to coach you throughout the procedure on demand and answer any questions you may have.

---

# 📖 Common Terms You May Hear

### 💊 Bronchodilator
Sometimes your healthcare provider may order breathing tests before and/or after using an inhaled medication to determine how your lungs respond to the medicine and determine the severity of issues in your lungs.

---

### 🌬️ DLCO
**Diffusing Capacity of the Lung for Carbon Monoxide** – Measures how efficiently gases move from the air sacs of your lungs into your bloodstream. Although the test uses a very tiny, safe amount of carbon monoxide for measurement purposes, it helps estimate how effectively oxygen would normally transfer into your blood.

---

### ⚡ FEV₁
**Forced Expiratory Volume in One Second** – The amount of air you can blow out during the **first second** of a forceful exhalation.

---

### 📊 FEV₁ / FVC Ratio
A comparison between FEV₁ and FVC. This helps doctors determine whether airflow obstruction may be present.

---

### 💨 FVC
**Forced Vital Capacity** – The total amount of air you can forcefully blast out after taking the deepest breath possible.

---

### 🫁 PFT
**Pulmonary Function Test** – A group of breathing tests that evaluate overall lung function.

---

### 🫁 Spirometry
Measures how much air you can breathe in and out and how quickly you can exhale. This part of the examination focuses on how deeply and forcefully you can exhale. My core purpose is to help you become comfortable with this part and making you more prepared.

---

### 🫁 Lung Volumes & TLC
Your lungs hold air in different "compartments." Think of it like a set of measuring cups:

- **Tidal Volume:** The air you breathe in and out with a normal, relaxed breath.
- **Inspiratory Reserve:** The extra air you can pull in after a normal breath in.
- **Expiratory Reserve:** The extra air you can push out after a normal breath out.
- **Residual Volume:** The air that always stays in your lungs (you cannot exhale this).

When you add all four of these volumes together, you get your **Total Lung Capacity (TLC)**—the grand total of air your lungs can hold. This is one of the most important numbers in your PFT report, helping your doctor understand if your lungs are expanding fully or if air is getting trapped.

---

# ⭐ Before We Begin

✔ Listen carefully to your respiratory therapist or my instructions.

✔ Take your time between attempts.

✔ If you become dizzy, uncomfortable, or need a break, please tell the staff immediately.

✔ Multiple attempts are normal.

✔ The goal is **not perfection**. The goal is obtaining reliable measurements through teamwork between you, your AI Companion, and your respiratory therapist.
"""
        # Toggle logic using state
        about_state = gr.State(False)
        about_btn.click(
            fn=lambda s: (not s, gr.update(visible=not s), about_content if not s else ""),
            inputs=[about_state],
            outputs=[about_state, about_box, about_box]
        )

        # --- MODE STATUS ---
        mode_status = gr.Markdown(
            value="🟠 **Practice Mode**",
            elem_classes="status-tag"
        )

        # Therapist
        with gr.Row():
            therapist_btn = gr.Button("👨‍⚕️ Request Respiratory Therapist", scale=2, elem_id="therapist-btn")
        therapist_box = gr.Markdown()

        # Record + Clear Buttons
        with gr.Row():
            mic_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Click RECORD when you hear 'One' (click STOP to score)",
                format="wav",
                scale=3,
                elem_classes="audio-wrap"
            )
            clear_btn = gr.Button(
                "✖ Clear Audio",
                scale=1,
                elem_id="clear-btn"
            )

        # Mode Buttons
        with gr.Row():
            practice_btn = gr.Button("🟠 Practice Mode", scale=2, elem_id="practice-btn")
            live_btn = gr.Button("🟣 Live AI Companion", scale=2, elem_id="live-btn")

        # --- BIG SCORE DISPLAY (Centered) ---
        gr.Markdown("---")
        gr.Markdown("### 📊 Instant Effort Score")
        with gr.Row():
            big_score_display = gr.Markdown(
                value="**0%**",
                elem_classes="big-score"
            )
        score_slider = gr.Slider(
            label="Overall Score (%)",
            minimum=0,
            maximum=100,
            step=1,
            value=0,
            interactive=False,
            scale=3
        )

        # --- UNIFIED ATTEMPT PROGRESS ---
        gr.Markdown("---")
        gr.Markdown("### 📈 Unified Attempt Progress (Practice + Live)")
        attempt_summary = gr.Markdown(value="No attempts recorded yet.")
        attempt_chart = gr.BarPlot(
            value=pd.DataFrame(columns=["Attempt", "Score"]),
            x="Attempt",
            y="Score",
            title="All Attempts (P=Practice, L=Live)",
            height=300
        )

        # --- DETAILED SUMMARY & TREND LIST (Side by side or stacked) ---
        gr.Markdown("---")
        gr.Markdown("### 📊 Detailed Summary & Trend")
        with gr.Row():
            detailed_summary_box = gr.Markdown(value="No attempts yet.", scale=1)
            trend_list_box = gr.Markdown(value="No attempts yet.", scale=1)

        # --- LIVE SESSION TRACKER ---
        gr.Markdown("---")
        gr.Markdown("### 📊 Live Session Tracker")
        attempt_counter = gr.Markdown(value="**Attempts:** 0 / 8")
        with gr.Row():
            reset_btn = gr.Button("🔄 Reset Live Session", visible=False, elem_id="reset-btn")

        # --- SESSION CONTROLS ---
        gr.Markdown("---")
        gr.Markdown("### 🎛️ Session Controls")
        with gr.Row():
            finish_btn = gr.Button("🔷 Finish Session", scale=2, elem_id="finish-btn")
        finish_box = gr.Markdown()

        # --- COACHING & RESULTS ---
        gr.Markdown("---")
        gr.Markdown("### 📝 Coaching & Results")
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

    # --- Record Change (10 outputs now) ---
    mic_input.change(
        fn=analyze_recording,
        inputs=[mic_input, current_mode, mode_status],
        outputs=[
            coach_box,            # 0: Report
            score_slider,         # 1: Score (for slider)
            attempt_chart,        # 2: Chart
            attempt_summary,      # 3: Summary text
            attempt_counter,      # 4: Counter
            reset_btn,            # 5: Reset visibility
            mic_input,            # 6: No-op
            detailed_summary_box, # 7: Detailed summary
            trend_list_box,       # 8: Trend list
            big_score_display     # 9: Big score number
        ]
    )

    # --- Clear Button ---
    clear_btn.click(
        fn=clear_mic,
        inputs=[],
        outputs=[mic_input]
    )

    # --- Reset Live ---
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

    return None

# --------------------------------------------------
# LAUNCH
# --------------------------------------------------
if __name__ == "__main__":
    print("🟢 6. Entering main block...")
    with gr.Blocks(title="PFT AI Companion V33") as demo:
        print("🟢 7. Building UI...")
        build_spirometry()
    print("🟢 8. UI built, launching now...")
    demo.launch(server_name="0.0.0.0", server_port=7863)
    print("🟢 9. Server should be running.")