"""
=========================================================
PFT AI Companion V32
Unified Live Module (with Instant Feedback)
=========================================================
"""

import time
import tempfile
import os
import uuid
import gradio as gr
from utils.Audio_Engine_v2 import AudioEngine
from gtts import gTTS

# --- For the Bar Graph ---
try:
    import matplotlib.pyplot as plt
    import io
    from PIL import Image
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️ Matplotlib not installed. Install with: pip install matplotlib")

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

MIN_DURATION = 6.0
MIN_EXPLOSION = 0.60
MIN_STABILITY = 0.70
MAX_ATTEMPTS = 8
PASSING_THRESHOLD = 80

# --------------------------------------------------
# COACHING SEQUENCE
# --------------------------------------------------

COACH_SEQUENCE = [
    (1.0, "# 🧘 Relax"),
    (1.0, "# Get Ready"),
    (1.5, "# 🫁 BIG DEEP BREATH"),
    (1.0, "# 3"),
    (1.0, "# 2"),
    (1.0, "# 1"),
    (1.0, "# 💨 BLAST!!"),
    (1.0, "# KEEP GOING"),
    (1.0, "# KEEP GOING"),
    (1.0, "# KEEP GOING"),
    (1.0, "# DON'T STOP"),
    (1.0, "# ALMOST THERE"),
    (1.0, "# FINISH"),
]

# --------------------------------------------------
# AUDIO ANALYSIS (No trimming)
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

    if total >= 95:
        stars = "⭐⭐⭐⭐⭐"
        base_advice = "Outstanding maneuver! You are ready for the real test."
    elif total >= 90:
        stars = "⭐⭐⭐⭐"
        base_advice = "Excellent blast. Try to sustain a little longer."
    elif total >= 80:
        stars = "⭐⭐⭐"
        base_advice = "Good effort. Keep exhaling longer to reach 6 seconds."
    else:
        stars = "⭐⭐"
        base_advice = "Keep practicing. Each attempt builds muscle memory."

    weak_points = []
    if blast < 70:
        weak_points.append("🔹 Explosive Start is low. Try a sharp, sudden cough-like burst.")
    if duration < 70:
        weak_points.append("🔹 Duration needs work. Focus on exhaling steadily for 6 seconds.")
    if stability < 70:
        weak_points.append("🔹 Consistency is dropping. Keep your airflow steady.")

    if weak_points:
        specific_advice = "\n\n### 💡 Where to Focus Next:\n" + "\n".join(weak_points)
    else:
        specific_advice = "\n\n🌟 You are performing well across all metrics!"

    report = f"""
### Performance
Explosive Start : **{blast:.0f}%**  
Duration : **{duration:.0f}%**  
Consistency : **{stability:.0f}%**

---

## {stars}

{base_advice}

**This Attempt Score:** # **{total}%**
{specific_advice}
"""
    return report, total

# --------------------------------------------------
# GENERATE AUDIO
# --------------------------------------------------

def generate_coach_audio():
    try:
        combined_text = " ".join([sentence for _, sentence in COACH_SEQUENCE])
        clean_text = combined_text.replace("#", "").replace("*", "").replace("🫁", "big deep breath").replace("💨", "blast")
        tts = gTTS(text=clean_text, lang="en", slow=False)
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "coach_prompt.mp3")
        tts.save(audio_path)
        time.sleep(0.5)
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            return audio_path
        return None
    except Exception as e:
        print(f"❌ Coach audio error: {e}")
        return None

def generate_welcome_audio():
    try:
        text = "Welcome to the Live AI Companion. Toggle the coach on or off, then click Record."
        tts = gTTS(text=text, lang="en", slow=False)
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "welcome_audio.mp3")
        tts.save(audio_path)
        time.sleep(0.5)
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            return audio_path
        return None
    except Exception as e:
        print(f"❌ Welcome audio error: {e}")
        return None

# --------------------------------------------------
# ATTEMPT GRAPH
# --------------------------------------------------

def generate_attempt_graph(attempts, passing_attempts, total_attempts):
    if not attempts or not MATPLOTLIB_AVAILABLE:
        return None
    fig, ax = plt.subplots(figsize=(8, max(2, len(attempts) * 0.6)))
    scores = [a[0] for a in attempts]
    labels = [f"#{i+1}" for i in range(len(attempts))]
    colors = ['#2ecc71' if a[1] else '#e74c3c' for a in attempts]
    y_pos = range(len(scores))
    ax.barh(y_pos, scores, color=colors, height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Score (%)')
    ax.set_title(f'Attempt History (Passing: {len(passing_attempts)} / 3)')
    ax.set_xlim([0, 100])
    ax.axvline(x=PASSING_THRESHOLD, color='blue', linestyle='--', label=f'Passing Threshold ({PASSING_THRESHOLD}%)')
    ax.legend()
    for i, s in enumerate(scores):
        status = 'PASS' if s >= PASSING_THRESHOLD else 'TRY AGAIN'
        ax.text(s + 2, i, f'{s:.0f}% {status}', va='center', fontsize=9)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# --------------------------------------------------
# STATUS UPDATE
# --------------------------------------------------

def update_status(state):
    if state.get("test_complete", False):
        return "🏁 Test Complete. Press 'Reset' to start over."
    total = state.get("total_attempts", 0)
    passing = len(state.get("passing_attempts", []))
    if total == 0:
        return "🟢 **Ready.** Click Record to start."
    remaining = MAX_ATTEMPTS - total
    need = 3 - passing
    if need <= 0:
        return "✅ You have enough passing attempts! Press 'Reset' to start a new session."
    return f"📊 **Attempt {total+1} of {MAX_ATTEMPTS}** | Need {need} more passing blow(s). {remaining} chances left."

# --------------------------------------------------
# RECORD CHANGE HANDLER (Instant Scoring)
# --------------------------------------------------

def on_record_change(audio_filepath, session_state, coach_toggle):
    # Return 8 outputs: reset_btn, feedback_box, coach_box, audio_output, session_state, graph, status, mic_input
    if session_state.get("test_complete", False):
        return (
            gr.update(visible=True),
            "✅ Test complete. Press Reset.",
            "# 🎯 Session Locked",
            None,
            session_state,
            None,
            "🏁 Test Complete.",
            None
        )
    if audio_filepath is None or not os.path.exists(audio_filepath):
        return (
            gr.update(visible=True),
            "⚠️ No recording. Click Record.",
            "# 🎤 Waiting...",
            None,
            session_state,
            None,
            "⚠️ No recording.",
            None
        )
    # Analyze
    features = analyze_audio(audio_filepath)
    report, score = evaluate_attempt(features)
    is_passing = score >= PASSING_THRESHOLD
    session_state["total_attempts"] += 1
    session_state["attempts"].append((score, is_passing))
    if is_passing:
        session_state["passing_attempts"].append(score)
    
    passing_count = len(session_state["passing_attempts"])
    total_count = session_state["total_attempts"]
    graph_img = generate_attempt_graph(session_state["attempts"], session_state["passing_attempts"], session_state["total_attempts"])
    status = update_status(session_state)
    
    # Check exit
    if passing_count >= 3:
        avg = sum(session_state["passing_attempts"]) / passing_count
        session_state["test_complete"] = True
        final_report = f"# 🎉 VALID TEST COMPLETE!\n\nYou achieved **{passing_count}** passing attempts out of {total_count}.\n\n**Final Score: {avg:.0f}%**\n\n{report}"
        return (
            gr.update(visible=True),
            f"✅ VALID! Passing: {passing_count}/3 | Final: {avg:.0f}%",
            final_report,
            None,
            session_state,
            graph_img,
            "🏁 Test Complete. Press Reset.",
            None
        )
    elif total_count >= MAX_ATTEMPTS:
        session_state["test_complete"] = True
        final_report = f"# ❌ Max Attempts Reached\n\nYou completed {total_count} attempts but only {passing_count} passing blows.\n\n{report}"
        return (
            gr.update(visible=True),
            f"❌ Max attempts. Passing: {passing_count}/3",
            final_report,
            None,
            session_state,
            graph_img,
            "🏁 Max attempts. Press Reset.",
            None
        )
    else:
        remaining = MAX_ATTEMPTS - total_count
        need = 3 - passing_count
        status = f"✅ Attempt {total_count} done! Score: {score}%. {remaining} chances left. Need {need} more passing blow(s)."
        return (
            gr.update(visible=True),
            f"Attempt {total_count}/{MAX_ATTEMPTS} | Passing: {passing_count}/3 | Need {need} more",
            report,
            None,
            session_state,
            graph_img,
            status,
            None
        )

# --------------------------------------------------
# COACH TOGGLE
# --------------------------------------------------

def toggle_coach(current):
    new_state = not current
    if new_state:
        return new_state, gr.update(value="🔊 Coach: ON (Click to turn OFF)", elem_classes="coach-toggle"), "🟢 Guided Mode ON."
    else:
        return new_state, gr.update(value="🔊 Coach: OFF (Click to turn ON)", elem_classes="coach-toggle-off"), "🟢 Unguided Mode."

# --------------------------------------------------
# RESET
# --------------------------------------------------

def reset_session():
    new_state = {
        "attempts": [],
        "passing_attempts": [],
        "total_attempts": 0,
        "test_complete": False
    }
    return ("", "", gr.update(visible=False), None, new_state, "🔄 Reset. Click Record to begin.")

# --------------------------------------------------
# BUILD UI
# --------------------------------------------------

def build_unified_module():
    session_state = gr.State({
        "attempts": [],
        "passing_attempts": [],
        "total_attempts": 0,
        "test_complete": False
    })
    coach_toggle = gr.State(False)
    
    with gr.Column():
        gr.HTML("""
        <style>
            .big-mic .wrap { height: auto !important; min-height: 130px !important; }
            .big-mic .record-button {
                height: 100px !important;
                font-size: 28px !important;
                min-width: 250px !important;
                background-color: #f39c12 !important;
                color: white !important;
                border-radius: 20px !important;
                margin: 10px !important;
                border: 3px solid #d68910 !important;
            }
            .big-mic .record-button:hover { background-color: #e67e22 !important; transform: scale(1.02); }
            .coach-toggle {
                background-color: #28a745 !important;
                color: white !important;
                font-size: 18px !important;
                padding: 12px !important;
                border-radius: 12px !important;
                border: 2px solid #1e7e34 !important;
            }
            .coach-toggle-off {
                background-color: #6c757d !important;
                color: white !important;
                font-size: 18px !important;
                padding: 12px !important;
                border-radius: 12px !important;
                border: 2px solid #5a6268 !important;
            }
            .coach-toggle:hover, .coach-toggle-off:hover { transform: scale(1.02); }
            .status-box {
                border: 2px solid #007bff !important;
                border-radius: 10px !important;
                padding: 12px !important;
                background-color: #f0f8ff !important;
                font-size: 16px !important;
                font-weight: bold !important;
            }
        </style>
        """)
        gr.Markdown("# 🎯 Unified Live Companion")
        welcome_audio = generate_welcome_audio()
        if welcome_audio:
            gr.Audio(value=welcome_audio, label="🔊 Welcome", visible=True, interactive=False, autoplay=True)
        
        with gr.Row():
            toggle_btn = gr.Button("🔊 Coach: OFF (Click to turn ON)", elem_classes="coach-toggle-off")
        
        status_box = gr.Markdown("🟢 **Ready.** Click Record to start.", elem_classes="status-box")
        
        with gr.Row():
            mic_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Click RECORD (click again to STOP & SCORE)", format="wav", scale=2, elem_classes="big-mic")
        
        feedback_box = gr.Markdown("")
        attempt_graph = gr.Image(label="📊 Attempt History", visible=True)
        coach_box = gr.Markdown("", height=200)
        audio_output = gr.Audio(visible=False)  # dummy
        
        with gr.Row():
            reset_btn = gr.Button("🔄 Reset Session", variant="secondary")
    
    # Bindings
    toggle_btn.click(
        fn=toggle_coach,
        inputs=[coach_toggle],
        outputs=[coach_toggle, toggle_btn, status_box]
    )
    mic_input.change(
        fn=on_record_change,
        inputs=[mic_input, session_state, coach_toggle],
        outputs=[reset_btn, feedback_box, coach_box, audio_output, session_state, attempt_graph, status_box, mic_input]
    )
    reset_btn.click(
        fn=reset_session,
        inputs=[],
        outputs=[coach_box, feedback_box, reset_btn, attempt_graph, session_state, status_box]
    )
    return None