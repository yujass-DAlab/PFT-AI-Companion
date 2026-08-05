"""
=========================================================
Spirometry V33 – Unified Single Page (Final)
Practice & Live AI Companion on One Screen

Author:
Jasmien Yu, DeepSeek

Educational prototype only.
Not intended for diagnosis or replacement of
clinical judgement.
=========================================================
"""

import time
import gradio as gr
import numpy as np
import pandas as pd
import pyttsx3
from utils.Audio_Engine_v2 import AudioEngine

# --------------------------------------------------
# TTS (Thread-Safe, Sequential)
# --------------------------------------------------

_lock = threading.Lock()

def speak(text):
    """
    Speaks text sequentially. Waits for the speech to finish before returning.
    """
    if not text:
        return
    with _lock:
        try:
            engine = pyttsx3.init()
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
# COACHING SCRIPT (with TTS)
# --------------------------------------------------

COACH_SEQUENCE = [
    (1.0, "# 🫁 BIG DEEP BREATH", "Take a big deep breath in."),
    (1.0, "# Get Ready", "Get ready."),
    (1.0, "# 3", "Three."),
    (1.0, "# 2", "Two."),
    (1.0, "# 1", "One. Click Record now."),
    (1.0, "# 💨 BLAST!!", "Blast out fast and hard!"),
    (1.0, "# KEEP GOING", "Keep going."),
    (1.0, "# KEEP GOING", "Keep going."),
    (1.0, "# KEEP GOING", "Keep going."),
    (1.0, "# DON'T STOP", "Don't stop."),
    (1.0, "# ALMOST THERE", "Almost there."),
    (1.0, "# FINISH", "Finish."),
]

# --------------------------------------------------
# REAL AUDIO ANALYSIS
# --------------------------------------------------

def analyze_audio(audio_filepath):
    if audio_filepath is None:
        return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}
    return AudioEngine.extract_features(audio_filepath)

def evaluate_attempt(features):
    blast = min(features["explosion"] / MIN_EXPLOSION, 1.0) * 100
    duration = min(features["duration"] / MIN_DURATION, 1.0) * 100
    stability = min(features["stability"] / MIN_STABILITY, 1.0) * 100
    total = round(blast * 0.50 + duration * 0.30 + stability * 0.20)

    if total >= 95:
        stars = "⭐⭐⭐⭐⭐"
        advice = "Outstanding maneuver. You are ready for the real test!"
        blast_pass = "✅"
        duration_pass = "✅"
        stability_pass = "✅"
    elif total >= 90:
        stars = "⭐⭐⭐⭐"
        advice = "Excellent blast. Try to sustain a little longer."
        blast_pass = "✅"
        duration_pass = "⏳" if duration < 80 else "✅"
        stability_pass = "⏳" if stability < 80 else "✅"
    elif total >= 80:
        stars = "⭐⭐⭐"
        advice = "Good effort. Keep exhaling longer to reach 6 seconds."
        blast_pass = "✅" if blast >= 80 else "⏳"
        duration_pass = "⏳" if duration < 80 else "✅"
        stability_pass = "⏳" if stability < 80 else "✅"
    else:
        stars = "⭐⭐"
        advice = "Keep practicing. Each attempt builds muscle memory."
        blast_pass = "⏳" if blast < 80 else "✅"
        duration_pass = "⏳" if duration < 80 else "✅"
        stability_pass = "⏳" if stability < 80 else "✅"

    pass_fail = f"**Pass/Fail:** Blast {blast_pass} | Duration {duration_pass} | Stability {stability_pass}"

    report = f"""
### Performance

Explosive Start : **{blast:.0f}%**

Duration : **{duration:.0f}%**

Consistency : **{stability:.0f}%**

---

## {stars}

{advice}

{pass_fail}

Overall Score:

# **{total}%**
"""
    return report

# --------------------------------------------------
# COACHING FLOW (Fast, Step-by-Step Streaming)
# --------------------------------------------------

def run_coaching_flow(audio_filepath, mode="practice"):
    """
    Streams the coaching text step-by-step, then analyzes the audio.
    """
    coach_text = ""
    for delay, sentence, tts_text in COACH_SEQUENCE:
        coach_text += sentence + "\n\n"
        speak(tts_text)
        yield coach_text  # Yield after each step (FAST PROMPT!)
        time.sleep(delay)

    # Analyze audio
    features = analyze_audio(audio_filepath)
    report = evaluate_attempt(features)
    if mode == "live":
        report += "\n\n✅ Live maneuver completed."

    yield report

# --------------------------------------------------
# PRACTICE MODE
# --------------------------------------------------

def run_practice(audio_filepath):
    # Show the retry button immediately
    yield (
        gr.update(visible=True),  # retry_btn
        gr.update(visible=False), # feedback_box
        "",                       # coach_box
        "",                       # feedback_box (placeholder)
        0                         # score_slider
    )

    # Stream coaching step-by-step
    coach_gen = run_coaching_flow(audio_filepath, mode="practice")
    for step in coach_gen:
        if "### Performance" in step:  # Report
            yield (
                gr.update(visible=True),
                gr.update(visible=True),
                "",
                step,
                0
            )
        else:  # Coaching text
            yield (
                gr.update(visible=True),
                gr.update(visible=False),
                step,
                "",
                0
            )

    # Extract score for the slider
    try:
        score_line = step.split("Overall Score:")[1].split("#")[1].strip().replace("**", "").replace("%", "")
        score = int(score_line)
    except:
        score = 0

    # Final update: show feedback and score slider
    yield (
        gr.update(visible=True),
        gr.update(visible=True),
        step,
        step,
        score
    )

# --------------------------------------------------
# LIVE MODE (with Attempt Tracking & Bar Chart)
# --------------------------------------------------

live_attempts = []

def run_live(audio_filepath):
    global live_attempts

    if len(live_attempts) >= MAX_ATTEMPTS:
        yield (
            gr.update(visible=True),
            gr.update(visible=False),
            "# ⛔ Maximum attempts reached.\nYou have completed 8 attempts.",
            "",
            gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
            gr.update(value=f"**Attempts:** {len(live_attempts)} / {MAX_ATTEMPTS}"),
            0
        )
        return

    # Show the live retry button immediately
    yield (
        gr.update(visible=True),   # live_retry_btn
        gr.update(visible=False),  # feedback_box
        "# Live Coaching Ready...\n",  # coach_box
        "",                        # feedback_box (placeholder)
        gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
        gr.update(value=f"**Attempts:** {len(live_attempts)+1} / {MAX_ATTEMPTS}"),
        0
    )

    # Stream coaching step-by-step
    coach_gen = run_coaching_flow(audio_filepath, mode="live")
    for step in coach_gen:
        if "### Performance" in step:  # Report
            yield (
                gr.update(visible=True),
                gr.update(visible=True),
                "",
                step,
                gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
                gr.update(value=f"**Attempts:** {len(live_attempts)+1} / {MAX_ATTEMPTS}"),
                0
            )
        else:  # Coaching text
            yield (
                gr.update(visible=True),
                gr.update(visible=False),
                step,
                "",
                gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
                gr.update(value=f"**Attempts:** {len(live_attempts)+1} / {MAX_ATTEMPTS}"),
                0
            )

    # Extract score for the slider and chart
    try:
        score_line = step.split("Overall Score:")[1].split("#")[1].strip().replace("**", "").replace("%", "")
        score = int(score_line)
    except:
        score = 0

    live_attempts.append(score)

    chart_data = pd.DataFrame({
        "Attempt": list(range(1, len(live_attempts) + 1)),
        "Score": live_attempts
    })

    # Final update: show feedback, score slider, and bar chart
    yield (
        gr.update(visible=True),
        gr.update(visible=True),
        step,
        step,
        gr.update(value=chart_data),
        gr.update(value=f"**Attempts:** {len(live_attempts)} / {MAX_ATTEMPTS}"),
        score
    )

def reset_live():
    global live_attempts
    live_attempts = []
    return (
        "",
        "",
        gr.update(visible=False),
        "",
        gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
        gr.update(value="**Attempts:** 0 / 8"),
        0
    )

# --------------------------------------------------
# THERAPIST HANDOFF
# --------------------------------------------------

def request_therapist():
    speak("A respiratory therapist has been notified.")
    return """
# 👨‍⚕️ Respiratory Therapist Requested

Your respiratory therapist has now been requested.

The AI Companion will remain available for
education and encouragement, while the
therapist directs the maneuver.

Please follow your therapist's instructions.
"""

# --------------------------------------------------
# SESSION COMPLETE
# --------------------------------------------------

def finish_session():
    speak("Session complete. Excellent effort.")
    return """
# 🎉 Session Complete

Excellent effort today.

Remember:

Every maneuver teaches your lungs
how to perform the test better.

Thank you for practicing with
AI Spirometry Companion.
"""

# --------------------------------------------------
# BUILD UI (Unified Single Page)
# --------------------------------------------------

def build_spirometry():
    with gr.Column():

        gr.Markdown("""
# 🫁 AI Spirometry Companion (V33)

**One page. Two modes. One click.**
""")

        # ---- Massive Record Button ----
        with gr.Row():
            mic_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Click RECORD, then choose a mode below",
                format="wav",
                scale=3,
                height=100
            )

        # ---- Mode Buttons (Large, Colored) ----
        with gr.Row():
            practice_btn = gr.Button(
                "🟢 Practice Mode",
                variant="primary",
                scale=3
            )
            live_btn = gr.Button(
                "🔵 Live AI Companion",
                variant="primary",
                scale=3
            )

        # ---- Instant Score Slider (Mid-Screen, Instant Feedback) ----
        gr.Markdown("---")
        gr.Markdown("### 📊 Instant Effort Score")
        score_slider = gr.Slider(
            label="Overall Score (%)",
            minimum=0,
            maximum=100,
            step=1,
            value=0,
            interactive=False,
            scale=3
        )

        # ---- Live Attempt Progress (Bar Chart) ----
        gr.Markdown("---")
        gr.Markdown("### 📈 Live Attempt Progress")
        attempt_counter = gr.Markdown(value="**Attempts:** 0 / 8")
        attempt_chart = gr.BarPlot(
            value=pd.DataFrame(columns=["Attempt", "Score"]),
            x="Attempt",
            y="Score",
            title="Progress Over Attempts",
            height=200
        )

        # ---- Coaching & Feedback ----
        coach_box = gr.Markdown(value="", height=300)
        feedback_box = gr.Markdown(value="", visible=False)

        # ---- Therapist & Finish (Colored) ----
        with gr.Row():
            therapist_btn = gr.Button(
                "👨‍⚕️ Request Respiratory Therapist",
                variant="primary",
                scale=2
            )
            finish_btn = gr.Button(
                "🔴 Finish Session",
                variant="primary",
                scale=2
            )

        therapist_box = gr.Markdown()
        finish_box = gr.Markdown()

        therapist_btn.click(
            fn=request_therapist,
            outputs=therapist_box
        )
        finish_btn.click(
            fn=finish_session,
            outputs=finish_box
        )

        # ---- Reset Buttons ----
        with gr.Row():
            retry_btn = gr.Button("🔄 Next Attempt (Practice)", visible=False)
            live_retry_btn = gr.Button("🔄 Reset Live Session", visible=False)

        # ---- Events ----
        practice_btn.click(
            fn=run_practice,
            inputs=[mic_input],
            outputs=[retry_btn, feedback_box, coach_box, feedback_box, score_slider]
        )

        retry_btn.click(
            fn=run_practice,
            inputs=[mic_input],
            outputs=[retry_btn, feedback_box, coach_box, feedback_box, score_slider]
        )

        live_btn.click(
            fn=run_live,
            inputs=[mic_input],
            outputs=[
                live_retry_btn,
                feedback_box,
                coach_box,
                feedback_box,
                attempt_chart,
                attempt_counter,
                score_slider
            ]
        )

        live_retry_btn.click(
            fn=reset_live,
            inputs=[],
            outputs=[
                coach_box,
                feedback_box,
                live_retry_btn,
                feedback_box,
                attempt_chart,
                attempt_counter,
                score_slider
            ]
        )

        # ---- Disclaimer ----
        gr.Markdown("---")
        gr.Markdown("⚠️ **Disclaimer:** Educational purposes only. Not a substitute for professional clinical judgment or diagnosis.")

    return None

# --------------------------------------------------
# GRADIO LAUNCH
# --------------------------------------------------
if __name__ == "__main__":
    with gr.Blocks(title="PFT AI Companion V33") as demo:
        build_spirometry()
    demo.launch(server_name="0.0.0.0", server_port=7863)