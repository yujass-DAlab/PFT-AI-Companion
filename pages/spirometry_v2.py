"""
============================================================
PFT AI Companion V2.1
spirometry_v2.py

Author: Jasmine Yu, ChatGPT, DeepSeek

Purpose:
Practice mode – three-step panel with unlimited attempts.
Tracks session stats and step-based progress (Step 1–4 per attempt).
============================================================
"""
import gradio as gr
import threading
import pyttsx3
from utils.Audio_Engine_v2 import AudioEngine

# --- TTS ---
_lock = threading.Lock()

def speak(text):
    if not text:
        return
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"⚠️ TTS error: {e}")
    threading.Thread(target=_speak, daemon=True).start()

# --- Configuration ---
MIN_DURATION = 6.0
MIN_EXPLOSION = 0.60
MIN_STABILITY = 0.70

# --- Audio Analysis ---
def analyze_audio(audio):
    return AudioEngine.extract_features(audio)

# --- Weighted Scoring ---
def evaluate_weighted(features):
    blast_score = min((features["explosion"] / MIN_EXPLOSION) * 100, 110)
    duration_score = min((features["duration"] / MIN_DURATION) * 100, 110)
    stability_score = min((features["stability"] / MIN_STABILITY) * 100, 110)

    total_weight = 1.5 + 1.0 + 0.5
    overall = (blast_score * 1.5 + duration_score * 1.0 + stability_score * 0.5) / total_weight

    issues = []
    if features["explosion"] < MIN_EXPLOSION * 0.85:
        issues.append("explosion")
    if features["duration"] < MIN_DURATION * 0.80:
        issues.append("duration")
    if features["stability"] < MIN_STABILITY * 0.70:
        issues.append("stability")

    return overall, issues

# --- Feedback ---
def feedback(score, issues):
    msgs = []

    if score >= 100:
        msgs.append("🎯 Perfect! You hit every target exactly. This is a textbook maneuver.")
    elif score >= 90:
        msgs.append("🌟 Outstanding! You met all three criteria—just a tiny bit more polish and it would be perfect.")
    elif score >= 80:
        msgs.append("👏 Excellent! You are very close to hitting all targets.")
    elif score >= 65:
        msgs.append("👍 Good attempt! Focus on the areas below to improve.")
    elif score >= 50:
        msgs.append("💪 Fair attempt! Keep practicing—you are building muscle memory.")
    else:
        msgs.append("🔄 That was a good warm-up. Let's try again—each blow tends to get better.")

    if "explosion" in issues:
        msgs.append("💨 Try to start your blast more explosively.")
    if "duration" in issues:
        msgs.append("🫁 Aim to sustain your blow a little longer (target: ≥ 6 seconds).")
    if "stability" in issues:
        msgs.append("🌬 Work on making your airflow smoother and more continuous.")

    if not issues and score < 100:
        msgs.append("🎉 Wonderful! You met all three criteria—great control.")

    return "\n\n".join(msgs)

# --- Progress Helper ---
def get_progress_text(step):
    return f"**Step {step} of 4**"

# --- Session State ---
def init_session_state():
    return {
        "attempts": 0,
        "best_blast_score": 0.0,
        "best_duration": 0.0,
        "blast_met": False,
        "duration_met": False,
        "stability_met": False,
        "current_step": 1  # 1, 2, 3, 4 (reset after 4)
    }

def update_session_summary(state, blast_score, duration, stability):
    state["attempts"] += 1
    state["best_blast_score"] = max(state["best_blast_score"], blast_score)
    state["best_duration"] = max(state["best_duration"], duration)

    if blast_score >= MIN_EXPLOSION:
        state["blast_met"] = True
    if duration >= MIN_DURATION:
        state["duration_met"] = True
    if stability >= MIN_STABILITY:
        state["stability_met"] = True

    blast_pct = int(state["best_blast_score"] * 100)
    lines = [
        "🏆 **Current Progress**",
        f"**Practices:** {state['attempts']}",
        f"**Best Blast Score:** {blast_pct}%",
        f"**Best Sustain:** {state['best_duration']:.1f} seconds",
        "",
        "**Progress Tracker:**"
    ]
    lines.append("✔ Explosive Start" if state["blast_met"] else "⏳ Explosive Start (keep practicing)")
    lines.append("✔ Duration" if state["duration_met"] else "⏳ Duration (aim for ≥ 6s)")
    lines.append("✔ Smoother Airflow" if state["stability_met"] else "⏳ Smoother Airflow")
    lines.append("\nThank you! Keep practicing to build confidence for your PFT.")
    return "\n".join(lines), state

# --- Step Functions ---
def step1_prompt(state):
    speak("Breathe in deeply. Fill your lungs all the way.")
    state["current_step"] = 2
    return "🌬️ Breathe in deeply. Fill your lungs all the way.", get_progress_text(2), state

def step2_blast(audio, state):
    if audio is None:
        return "⚠️ No audio recorded.", "", 0, state
    features = analyze_audio(audio)
    score, issues = evaluate_weighted(features)
    msg = feedback(score, issues)
    blast_score = features["explosion"]
    summary_text, new_state = update_session_summary(
        state, blast_score, features["duration"], features["stability"]
    )
    new_state["current_step"] = 3
    return msg, f"💨 Blast Effort: {blast_score:.2f}", int(blast_score * 100), new_state, get_progress_text(3)

def step3_sustain(audio, state):
    if audio is None:
        return "⚠️ No audio recorded.", "", 0.0, state
    features = analyze_audio(audio)
    score, issues = evaluate_weighted(features)
    msg = feedback(score, issues)
    duration = features["duration"]
    summary_text, new_state = update_session_summary(
        state, state["best_blast_score"], duration, features["stability"]
    )
    new_state["current_step"] = 4
    return msg, f"⏱️ Duration: {duration:.1f}s", duration, new_state, get_progress_text(4)

def finalize_practice(state):
    # Mark practice as complete and reset step to 1 for next round
    state["current_step"] = 1
    return "✅ Practice complete! Click 'Start Over' or continue.", get_progress_text(1), state

# --- Reset ---
def reset_practice():
    speak("Resetting. Let's start over.")
    return (
        "", "", "", "", "", 0, 0.0,
        get_progress_text(1),
        "🏆 **Session Complete**\nComplete your first attempt to see progress!",
        init_session_state()
    )

# --- Build UI ---
def build_spirometry():
    with gr.Column():
        session_state = gr.State(value=init_session_state())

        gr.Markdown("# 🫁 Practice Mode")
        gr.Markdown("**Follow the three steps below.** Practice as many times as you **want**.")

        progress_box = gr.Markdown(get_progress_text(1))

        # -------- Step 1: Breathe In Deeply --------
        gr.Markdown("## 🌬️ Step 1: Breathe In Deeply")
        gr.Markdown("*💡 Why: Maximizing your air intake ensures a full starting volume for the test.*")
        with gr.Row():
            btn1 = gr.Button("🎧 Listen to Instruction", variant="primary")
            instr_box = gr.Textbox(label="Instruction", interactive=False, lines=2)

        btn1.click(
            step1_prompt,
            inputs=[session_state],
            outputs=[instr_box, progress_box, session_state]
        )

        # -------- Step 2: Blast Out --------
        gr.Markdown("## 💨 Step 2: Blast Out")
        gr.Markdown("*💡 Why: The first second of your blow (FEV1) is the most critical measurement. A fast start is key.*")
        with gr.Row():
            mic_blast = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Record your blast",
                format="wav"
            )
            blast_btn = gr.Button("📊 Analyze My Blast", variant="secondary")
            blast_feedback = gr.Textbox(label="Feedback", interactive=False, lines=3)
            blast_summary = gr.Textbox(label="Summary", interactive=False, lines=1)
            blast_progress = gr.Slider(label="Blast Effort (%)", minimum=0, maximum=100, step=1, interactive=False)

        blast_btn.click(
            step2_blast,
            inputs=[mic_blast, session_state],
            outputs=[blast_feedback, blast_summary, blast_progress, session_state, progress_box]
        )

        # -------- Step 3: Sustain --------
        gr.Markdown("## ⏱️ Step 3: Sustain")
        gr.Markdown("*💡 Why: **Keep blowing for at least 6 seconds** to confirm your airways are clear and unobstructed.*")
        with gr.Row():
            mic_sustain = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Record your sustain",
                format="wav"
            )
            sustain_btn = gr.Button("📊 Analyze My Sustain", variant="secondary")
            sustain_feedback = gr.Textbox(label="Feedback", interactive=False, lines=3)
            sustain_summary = gr.Textbox(label="Summary", interactive=False, lines=2)
            sustain_progress = gr.Slider(label="Duration Progress (0-10s)", minimum=0, maximum=10, step=0.1, interactive=False)

        sustain_btn.click(
            step3_sustain,
            inputs=[mic_sustain, session_state],
            outputs=[sustain_feedback, sustain_summary, sustain_progress, session_state, progress_box]
        )

        # -------- Session Summary --------
        gr.Markdown("---")
        session_box = gr.Markdown(label="📊 Session Summary", value="🏆 **Session Complete**\nComplete your first attempt to see progress!")

        # -------- Reminder --------
        gr.Markdown(
            """
            💡 **Tip:** To clear a recording, click the **"X"** on the top-right of the audio box.  
            Click **"Start Over"** below to clear the session stats and progress.
            """
        )

        # -------- Navigation --------
        with gr.Row():
            reset_btn = gr.Button("🔄 Start Over", variant="stop", scale=1)
            go_live_btn = gr.Button("➡️ Go to Live AI Companion", variant="secondary", scale=1)

        # -------- Events --------
        blast_btn.click(
            lambda state: (update_session_summary(state, state["best_blast_score"], state["best_duration"], state["stability_met"])[0], state),
            inputs=[session_state],
            outputs=[session_box, session_state]
        )

        sustain_btn.click(
            lambda state: (update_session_summary(state, state["best_blast_score"], state["best_duration"], state["stability_met"])[0], state),
            inputs=[session_state],
            outputs=[session_box, session_state]
        )

        reset_btn.click(
            reset_practice,
            inputs=[],
            outputs=[
                instr_box,
                blast_feedback,
                blast_summary,
                sustain_feedback,
                sustain_summary,
                blast_progress,
                sustain_progress,
                progress_box,
                session_box,
                session_state
            ]
        )

        gr.Markdown("---")
        gr.Markdown("⚠️ **Disclaimer:** Educational purposes only. Not a substitute for professional clinical judgment or diagnosis.")

    return reset_btn, go_live_btn