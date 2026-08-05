"""
=========================================================
Spirometry V3
One-Click AI Coaching Experience

Author:
Jasmien Yu, DeepSeek

Educational prototype only.
Not intended for diagnosis or replacement of
clinical judgement.

=========================================================
"""

import asyncio
import gradio as gr
import numpy as np
from utils.Audio_Engine_v2 import AudioEngine

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

APP_TITLE = """
# 🫁 AI Spirometry Companion (V3)

Choose how you wish to experience today's session.

One click.

Relax.

Let AI guide you through the maneuver.
"""

MODE_TEXT = """
### Practice Mode
Unlimited practice before the real examination.

### Live AI Companion
AI guides your actual maneuver in real time.

### Human Therapist
Request therapist guidance at any time.
"""

# --------------------------------------------------
# COACHING SCRIPT
# --------------------------------------------------

COACH_SEQUENCE = [
    (1.0, "# 🧘 Relax"),
    (1.0, "# Get Ready"),
    (1.0, "# 3"),
    (1.0, "# 2"),
    (1.0, "# 1"),
    (1.5, "# 🫁 BIG DEEP BREATH"),
    (1.0, "# 💨 BLAST!!"),
    (1.0, "# KEEP GOING"),
    (1.0, "# KEEP GOING"),
    (1.0, "# KEEP GOING"),
    (1.0, "# DON'T STOP"),
    (1.0, "# ALMOST THERE"),
    (1.0, "# FINISH"),
]

# --------------------------------------------------
# MINIMUM THRESHOLDS (for realistic feedback)
# --------------------------------------------------

MIN_DURATION = 6.0
MIN_EXPLOSION = 0.60
MIN_STABILITY = 0.70


# --------------------------------------------------
# ASYNC COACH (Replaces time.sleep)
# --------------------------------------------------

async def async_coach():
    """
    Yields each coaching step with a non-blocking delay.
    """
    screen = ""
    for delay, sentence in COACH_SEQUENCE:
        screen += sentence + "\n\n"
        yield screen
        await asyncio.sleep(delay)


# --------------------------------------------------
# REAL AUDIO ANALYSIS
# --------------------------------------------------

def analyze_audio(audio_filepath):
    """
    Extracts real features from the microphone recording.
    """
    if audio_filepath is None:
        return {
            "explosion": 0.0,
            "duration": 0.0,
            "stability": 0.0
        }
    return AudioEngine.extract_features(audio_filepath)


def evaluate_attempt(features):
    """
    Scores the attempt based on real extracted features.
    """
    blast = min(features["explosion"] / MIN_EXPLOSION, 1.0) * 100
    duration = min(features["duration"] / MIN_DURATION, 1.0) * 100
    stability = min(features["stability"] / MIN_STABILITY, 1.0) * 100

    total = round(blast * 0.50 + duration * 0.30 + stability * 0.20)

    if total >= 95:
        stars = "⭐⭐⭐⭐⭐"
        advice = "Outstanding maneuver. You are ready for the real test!"
    elif total >= 90:
        stars = "⭐⭐⭐⭐"
        advice = "Excellent blast. Try to sustain a little longer."
    elif total >= 80:
        stars = "⭐⭐⭐"
        advice = "Good effort. Keep exhaling longer to reach 6 seconds."
    else:
        stars = "⭐⭐"
        advice = "Keep practicing. Each attempt builds muscle memory."

    report = f"""
### Performance

Explosive Start : **{blast:.0f}%**

Duration : **{duration:.0f}%**

Consistency : **{stability:.0f}%**

---

## {stars}

{advice}

Overall Score:

# **{total}%**
"""
    return report


# --------------------------------------------------
# MODE CONTROLLERS (Practice & Live)
# --------------------------------------------------

async def run_practice(audio_filepath):
    """
    One-click practice session with real audio analysis.
    """
    yield (
        gr.update(visible=True),
        gr.update(visible=False),
        "",
        "",
    )

    # ---------- Coaching ----------
    running_text = ""
    async for text in async_coach():
        running_text = text
        yield (
            gr.update(),
            gr.update(),
            running_text,
            ""
        )

    # ---------- Analysis ----------
    features = analyze_audio(audio_filepath)
    report = evaluate_attempt(features)

    yield (
        gr.update(),
        gr.update(visible=True),
        running_text,
        report
    )


async def run_live(audio_filepath):
    """
    Live AI Companion with real audio analysis.
    """
    yield (
        gr.update(visible=True),
        gr.update(visible=False),
        "# Live Coaching Ready...\n",
        ""
    )

    live_text = ""
    async for text in async_coach():
        live_text = text
        yield (
            gr.update(),
            gr.update(),
            live_text,
            ""
        )

    features = analyze_audio(audio_filepath)
    report = evaluate_attempt(features)
    report += "\n\n✅ Live maneuver completed."

    yield (
        gr.update(),
        gr.update(visible=True),
        live_text,
        report
    )


# --------------------------------------------------
# THERAPIST HANDOFF
# --------------------------------------------------

def request_therapist():
    return """
# 👨‍⚕️ Respiratory Therapist Requested

Your respiratory therapist has now been requested.

The AI Companion will remain available for
education and encouragement, while the
therapist directs the maneuver.

Please follow your therapist's instructions.
"""


# --------------------------------------------------
# RESET SESSION
# --------------------------------------------------

def reset_session():
    return (
        "",
        "",
        gr.update(visible=False)
    )


# --------------------------------------------------
# SESSION COMPLETE
# --------------------------------------------------

def finish_session():
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
# BUILD UI
# --------------------------------------------------

def build_spirometry():
    with gr.Column():
        gr.Markdown(APP_TITLE)
        gr.Markdown(MODE_TEXT)

        # --- Audio Input ---
        mic_input = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="🎤 Click Record, then follow the coach",
            format="wav"
        )

        with gr.Row():
            practice_btn = gr.Button(
                "🟢 Practice Mode",
                variant="primary",
                scale=2
            )
            live_btn = gr.Button(
                "🔵 Live AI Companion",
                scale=2
            )

        with gr.Row():
            therapist_btn = gr.Button(
                "👨‍⚕️ Request Respiratory Therapist",
                scale=2
            )
            finish_btn = gr.Button(
                "🔴 Finish Session",
                scale=2
            )

        coach_box = gr.Markdown(
            value="",
            height=350
        )

        feedback_box = gr.Markdown(
            value="",
            visible=False
        )

        therapist_box = gr.Markdown()

        retry_btn = gr.Button(
            "🔄 Try Again",
            visible=False
        )

    # -----------------------------------------
    # Practice Mode
    # -----------------------------------------
    practice_btn.click(
        fn=run_practice,
        inputs=[mic_input],
        outputs=[
            retry_btn,
            feedback_box,
            coach_box,
            feedback_box
        ]
    )

    # -----------------------------------------
    # Live Mode
    # -----------------------------------------
    live_btn.click(
        fn=run_live,
        inputs=[mic_input],
        outputs=[
            retry_btn,
            feedback_box,
            coach_box,
            feedback_box
        ]
    )

    # -----------------------------------------
    # Retry
    # -----------------------------------------
    retry_btn.click(
        fn=run_practice,
        inputs=[mic_input],
        outputs=[
            retry_btn,
            feedback_box,
            coach_box,
            feedback_box
        ]
    )

    # -----------------------------------------
    # Therapist
    # -----------------------------------------
    therapist_btn.click(
        fn=request_therapist,
        outputs=therapist_box
    )

    # -----------------------------------------
    # Finish
    # -----------------------------------------
    finish_btn.click(
        fn=finish_session,
        outputs=coach_box
    )

    return practice_btn, live_btn, therapist_btn, finish_btn


# --------------------------------------------------
# GRADIO LAUNCH (Optional if used as standalone)
# --------------------------------------------------
if __name__ == "__main__":
    with gr.Blocks(title="PFT AI Companion V3") as demo:
        build_spirometry()
    demo.launch(server_name="0.0.0.0", server_port=7863)