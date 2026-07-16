"""
=========================================================
PFT AI Companion
live_assistant.py

Author: Jasmine Yu, ChatGPT, DeepSeek

Purpose:
Live AI Companion – three-step panel with "Start Live" and "Submit Live Attempt".
=========================================================
"""
import gradio as gr
import threading
import pyttsx3
from utils.Audio_Engine import AudioEngine

# --- TTS (Threaded, Fresh Engine) ---
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

# --- Evaluation ---
def evaluate(features):
    score = 100
    issues = []
    if features["explosion"] < MIN_EXPLOSION:
        score -= 25
        issues.append("explosion")
    if features["duration"] < MIN_DURATION:
        score -= 20
        issues.append("duration")
    if features["stability"] < MIN_STABILITY:
        score -= 15
        issues.append("stability")
    score = max(score, 0)
    return score, issues

def feedback(score, issues):
    msgs = []
    if score >= 90:
        msgs.append("🌟 Excellent! You are ready!")
    elif score >= 80:
        msgs.append("👏 Good effort!")
    elif score >= 65:
        msgs.append("👍 This was a good attempt.")
    else:
        msgs.append("💙 Ask your therapist for guidance.")
    if "explosion" in issues:
        msgs.append("💨 Start your blow more explosively.")
    if "duration" in issues:
        msgs.append("🫁 Try to sustain your blow a little longer.")
    if "stability" in issues:
        msgs.append("🌬 Aim for smoother airflow.")
    if not issues:
        msgs.append("🎉 Perfect maneuver!")
    return "\n\n".join(msgs)

# --- Step Functions ---
def step1_prompt():
    speak("Breathe in deeply. Fill your lungs all the way.")
    return "🌬️ Breathe in deeply. Fill your lungs all the way."

def step2_blast(audio):
    if audio is None:
        return "⚠️ No audio recorded.", ""
    features = analyze_audio(audio)
    score, issues = evaluate(features)
    msg = feedback(score, issues)
    summary = f"💨 Blast Effort: {features['explosion']:.2f} (target ≥ {MIN_EXPLOSION})"
    return msg, summary

def step3_sustain(audio):
    if audio is None:
        return "⚠️ No audio recorded.", ""
    features = analyze_audio(audio)
    score, issues = evaluate(features)
    msg = feedback(score, issues)
    summary = f"⏱️ Duration: {features['duration']:.1f}s (target ≥ {MIN_DURATION}s)\n🫁 Stability: {features['stability']:.2f} (target ≥ {MIN_STABILITY})"
    return msg, summary

# --- Live Test Controls ---
def start_live():
    speak("Live test started. Follow the three steps.")
    return "🎯 Live test started! Complete all three steps below, then click 'Submit Live Attempt'."

def submit_live():
    speak("Your live attempt has been submitted.")
    return "✅ Your live attempt has been submitted. Please discuss your results with your respiratory therapist."

# --- Reset (Clears Text + Audio) ---
def reset_live():
    speak("Resetting live test.")
    return (
        "",                           # status_box
        "",                           # instr_box
        "",                           # blast_feedback
        "",                           # blast_summary
        "",                           # sustain_feedback
        "",                           # sustain_summary
        "",                           # submit_box
        gr.update(value=None),        # mic_blast (clears waveform)
        gr.update(value=None)         # mic_sustain (clears waveform)
    )

# --- Build UI ---
def build_live_assistant():
    with gr.Column():
        gr.Markdown("# 🎯 Live AI Companion")
        gr.Markdown("**Complete the three steps below. This is your live test attempt.**")

        # -------- Start Live --------
        with gr.Row():
            start_btn = gr.Button("▶ Start Live Test", variant="primary")
            status_box = gr.Textbox(label="Status", interactive=False, lines=1)

        start_btn.click(start_live, inputs=[], outputs=[status_box])

        # -------- Step 1: Breathe In --------
        gr.Markdown("### 🌬️ Step 1: Breathe In")
        with gr.Row():
            btn1 = gr.Button("🎧 Hear Instruction", variant="primary")
            instr_box = gr.Textbox(label="Instruction", interactive=False, lines=2)

        btn1.click(step1_prompt, inputs=[], outputs=[instr_box])

        # -------- Step 2: Blast Out --------
        gr.Markdown("### 💨 Step 2: Blast Out")
        with gr.Row():
            mic_blast = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Record your blast",
                format="wav"
            )
            blast_btn = gr.Button("📊 Analyze Blast", variant="secondary")
            blast_feedback = gr.Textbox(label="Feedback", interactive=False, lines=3)
            blast_summary = gr.Textbox(label="Summary", interactive=False, lines=1)

        blast_btn.click(
            step2_blast,
            inputs=[mic_blast],
            outputs=[blast_feedback, blast_summary]
        )

        # -------- Step 3: Sustain --------
        gr.Markdown("### ⏱️ Step 3: Sustain")
        with gr.Row():
            mic_sustain = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Record your sustain",
                format="wav"
            )
            sustain_btn = gr.Button("📊 Analyze Sustain", variant="secondary")
            sustain_feedback = gr.Textbox(label="Feedback", interactive=False, lines=3)
            sustain_summary = gr.Textbox(label="Summary", interactive=False, lines=2)

        sustain_btn.click(
            step3_sustain,
            inputs=[mic_sustain],
            outputs=[sustain_feedback, sustain_summary]
        )

        # -------- Submit Live Attempt --------
        with gr.Row():
            submit_btn = gr.Button("📤 Submit Live Attempt", variant="primary")
            submit_box = gr.Textbox(label="Submission Status", interactive=False, lines=2)

        submit_btn.click(submit_live, inputs=[], outputs=[submit_box])

        # -------- Friendly Reminder --------
        gr.Markdown(
            """
            💡 **Tip:** Click **"Start Over"** below to clear previous stats and recordings before a new attempt.
            """
        )

        # -------- Navigation --------
        with gr.Row():
            reset_btn = gr.Button("🔄 Start Over", variant="stop", scale=1)
            go_practice_btn = gr.Button("➡️ Go to Practice Mode", variant="secondary", scale=1)

        # -------- Reset Logic (Clears Text + Audio) --------
        reset_btn.click(
            reset_live,
            inputs=[],
            outputs=[
                status_box,
                instr_box,
                blast_feedback,
                blast_summary,
                sustain_feedback,
                sustain_summary,
                submit_box,
                mic_blast,
                mic_sustain
            ]
        )

        gr.Markdown("---")
        gr.Markdown("⚠️ **Disclaimer:** Educational purposes only. Not for diagnosis.")

    # Return BOTH buttons for app.py to use
    return reset_btn, go_practice_btn