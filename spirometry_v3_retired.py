"""
=========================================================
Spirometry V3-retired – Unified Single Page (Final Revision)
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
from utils.Audio_Engine_v2 import AudioEngine
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
            import pyttsx3  # <-- Move import here
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
    # Checks if the user clicked Record AND if the file actually exists on disk.
    # (audio_filepath is None = no file selected. os.path.exists = file was saved properly.)
    if audio_filepath is None or not os.path.exists(audio_filepath):
        return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}
    return AudioEngine.extract_features(audio_filepath)

def evaluate_attempt(features):
    blast = min(features["explosion"] / MIN_EXPLOSION, 1.0) * 100
    duration = min(features["duration"] / MIN_DURATION, 1.0) * 100
    stability = min(features["stability"] / MIN_STABILITY, 1.0) * 100
    total = round(blast * 0.50 + duration * 0.30 + stability * 0.20)

    # ADVICE LOGIC (UPDATED to use 80% threshold for the weakest metric)
    # This prevents the contradiction of saying "performing well" while failing the test.
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

    # Stars and overall advice are based on the TOTAL weighted score (>=80 is PASS).
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
    return report, total

# --------------------------------------------------
# UNIFIED ATTEMPT HISTORY (Tracks ALL attempts)
# --------------------------------------------------

attempt_history = []  # Stores tuples: (score, mode)

def log_attempt(score, mode):
    attempt_history.append((score, mode))

def get_unified_chart():
    if not attempt_history:
        return pd.DataFrame(columns=["Attempt", "Score"])
    
    scores = [s[0] for s in attempt_history]
    modes = [s[1] for s in attempt_history]
    
    # Color coding: Practice = 🟠, Live = 🟣
    labels = [f"{i+1} ({'P' if m=='practice' else 'L'})" for i, m in enumerate(modes)]
    
    return pd.DataFrame({
        "Attempt": labels,
        "Score": scores
    })

def get_attempt_summary():
    if not attempt_history:
        return "No attempts recorded yet."
    
    total = len(attempt_history)
    practice_count = sum(1 for s, m in attempt_history if m == "practice")
    live_count = sum(1 for s, m in attempt_history if m == "live")
    passing = sum(1 for s, m in attempt_history if s >= 80)
    failing = total - passing
    
    return f"""
**Attempt Summary:**  
- **Total Blows:** {total}  
- **Practice:** {practice_count} | **Live:** {live_count}  
- **Passing (≥80%):** {passing} | **Failing (<80%):** {failing}
    """

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
# LIVE SESSION STATE (for 3/8 rule)
# --------------------------------------------------

live_session = {
    "total_attempts": 0,
    "attempts": []
}

def analyze_recording(audio_filepath, current_mode, status_text):
    """
    Triggered when user stops recording. Returns 7 outputs.
    The 7 outputs correspond to the ORDER in the outputs list of mic_input.change().
    """
    # 'global' tells Python we are modifying the outer variables, not creating new ones.
    global attempt_history, live_session

    if audio_filepath is None or not os.path.exists(audio_filepath):
        return (
            "⚠️ No recording detected. Click Record and try again.",
            0,
            gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
            get_attempt_summary(),
            "**Attempts:** 0 / 8",
            gr.update(visible=False),
            gr.update()  # mic placeholder (no-op)
        )

    try:
        features = analyze_audio(audio_filepath)
        report, score = evaluate_attempt(features)
    except Exception as e:
        return (
            f"❌ Error analyzing audio: {str(e)}. Please try again.",
            0,
            gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
            get_attempt_summary(),
            "**Attempts:** 0 / 8",
            gr.update(visible=False),
            gr.update()
        )

    # Log to UNIFIED history
    log_attempt(score, current_mode)
    
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
        # Practice mode – no limit, just update the counter to show total
        practice_count = sum(1 for s, m in attempt_history if m == "practice")
        counter_text = f"**Practice Attempts:** {practice_count}"
        reset_visible = gr.update(visible=False)

    # Build unified chart & summary
    chart_data = get_unified_chart()
    summary_text = get_attempt_summary()

    return (
        report,
        score,
        gr.update(value=chart_data),
        summary_text,
        counter_text,
        reset_visible,
        gr.update()  # Leave mic unchanged (no-op) to prevent infinite loop
    )

# --------------------------------------------------
# CLEAR MIC
# --------------------------------------------------

def clear_mic():
    """Clears the audio component. value=None resets the UI so the user can record a fresh blow."""
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
        gr.update()  # mic placeholder
    )

# --------------------------------------------------
# THERAPIST & FINISH (UPDATED WITH YOUR REASSURING WORDS)
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
    </style>
    """)

    with gr.Column():
        gr.Markdown("""
        #  AI Spirometry Companion (V3-retired)
        **One page. Two modes. All stats.**
        """)

        # --- ACCURATE INSTRUCTIONS (Includes Clear step) ---
        gr.Markdown("""
        ### 📋 How to Use (Step-by-Step)
        1. **Choose a mode** below → The coach speaks automatically.
        2. When you hear **"One"**, click the **red Record** button → Blow when you hear **"BLAST out!"**.
        3. Click the **Stop** button (the square ■) → **Your score appears instantly!**
        4. **To do the next attempt**: Click the **"✖ Clear"** button (next to Record) to reset the mic. Then, either:
           - Click **Record** again (if you remember the timing), OR
           - Click the **mode button** again (to hear the coach once more).
        """)

        # --- MODE STATUS ---
        mode_status = gr.Markdown(
            value="🟠 **Practice Mode**",
            elem_classes="status-tag"
        )

        # Therapist
        with gr.Row():
            therapist_btn = gr.Button("👨‍⚕️ Request Respiratory Therapist", scale=2, elem_id="therapist-btn")
        therapist_box = gr.Markdown()

        # Record + Clear Buttons (side-by-side)
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

        # Score & Progress
        gr.Markdown("---")
        gr.Markdown("### 📊 Instant Effort Score")
        score_slider = gr.Slider(label="Overall Score (%)", minimum=0, maximum=100, step=1, value=0, interactive=False, scale=3)

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
        
        gr.Markdown("---")
        gr.Markdown("### 📊 Live Session Tracker")
        attempt_counter = gr.Markdown(value="**Attempts:** 0 / 8")
        with gr.Row():
            reset_btn = gr.Button("🔄 Reset Live Session", visible=False, elem_id="reset-btn")

        # Session Controls
        gr.Markdown("---")
        gr.Markdown("### 🎛️ Session Controls")
        with gr.Row():
            finish_btn = gr.Button("🔷 Finish Session", scale=2, elem_id="finish-btn")
        finish_box = gr.Markdown()

        # Coaching & Results
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

    # --- Record Change (7 outputs) ---
    mic_input.change(
        fn=analyze_recording,
        inputs=[mic_input, current_mode, mode_status],
        outputs=[
            coach_box,        # 0: Report
            score_slider,     # 1: Score
            attempt_chart,    # 2: Chart (unified)
            attempt_summary,  # 3: Summary text
            attempt_counter,  # 4: Counter
            reset_btn,        # 5: Reset button visibility
            mic_input         # 6: No-op (gr.update())
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
            mic_input
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

