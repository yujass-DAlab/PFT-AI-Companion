"""
=========================================================
PFT AI Companion V31
Live AI Companion (FINAL - Status-Driven Workflow)
=========================================================
"""

import time
import tempfile
import os
import uuid
import numpy as np
import gradio as gr
from utils.Audio_Engine_v2 import AudioEngine
from gtts import gTTS

# --- For Audio Trimming ---
try:
    from scipy.io import wavfile
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("⚠️ Scipy not installed. Install with: pip install scipy")

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
# SMART AUDIO TRIMMING
# --------------------------------------------------

def trim_to_blow(input_filepath):
    if not SCIPY_AVAILABLE or not os.path.exists(input_filepath):
        return input_filepath
    try:
        rate, data = wavfile.read(input_filepath)
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        abs_data = np.abs(data)
        peak_idx = np.argmax(abs_data)
        start_idx = max(0, peak_idx - int(rate * 0.5))
        end_idx = min(len(data), peak_idx + int(rate * 2.0))
        trimmed_data = data[start_idx:end_idx]
        temp_dir = tempfile.gettempdir()
        unique_id = uuid.uuid4().hex[:6]
        trimmed_path = os.path.join(temp_dir, f"trimmed_blow_{unique_id}.wav")
        wavfile.write(trimmed_path, rate, trimmed_data.astype(np.int16))
        print(f"✂️ Trimmed blow saved to: {trimmed_path}")
        return trimmed_path
    except Exception as e:
        print(f"⚠️ Trimming failed: {e}")
        return input_filepath

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

def generate_welcome_audio():
    try:
        text = "Welcome! You can request a respiratory therapist, or start the live test with AI."
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

def generate_coach_audio():
    try:
        combined_text = " ".join([sentence for _, sentence in COACH_SEQUENCE])
        clean_text = combined_text.replace("#", "").replace("*", "").replace("🫁", "big deep breath").replace("💨", "blast")
        tts = gTTS(text=clean_text, lang="en", slow=False)
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "coach_prompt.mp3")
        tts.save(audio_path)
        time.sleep(0.5)
        print(f"🎤 Coach audio saved: {audio_path}")
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            return audio_path
        return None
    except Exception as e:
        print(f"❌ Coach audio error: {e}")
        return None

def generate_therapist_audio():
    try:
        text = "Your respiratory therapist has now been requested. Please follow your therapist's instructions."
        tts = gTTS(text=text, lang="en", slow=False)
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "therapist_request.mp3")
        tts.save(audio_path)
        time.sleep(0.3)
        return audio_path
    except Exception as e:
        print(f"❌ Therapist audio error: {e}")
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
# STEP 1: PLAY COACH
# --------------------------------------------------

def play_coach_sequence():
    audio_path = generate_coach_audio()
    if audio_path is None:
        yield "❌ Audio generation failed.", None, "⚠️ Error: No audio."
        return

    coach_text = ""
    for delay, sentence in COACH_SEQUENCE:
        coach_text += sentence + "\n\n"
        yield coach_text, audio_path, "🎧 Listening... Get ready to blow!"
        time.sleep(delay)

# --------------------------------------------------
# STEP 2: AUTO-ANALYZE ON RECORDING STOP
# --------------------------------------------------

def analyze_my_blow(audio_filepath, session_state):
    print(f"🔍 Auto-analyze triggered with file: {audio_filepath}")

    # Default statuses
    status_text = "⏳ Analyzing..."

    if session_state.get("test_complete", False):
        return (
            gr.update(visible=True),
            "✅ Test already complete. Press 'Reset' to start over.",
            "# 🎯 Session Locked",
            None,
            session_state,
            None,
            "🔄 Test Complete. Press 'Reset'.",
            None  # Mic output (keep as is)
        )

    if audio_filepath is None or not os.path.exists(audio_filepath):
        status_text = "⚠️ No recording found. Click the orange button to start."
        return (
            gr.update(visible=True),
            "⚠️ No recording.",
            "# 🎤 Waiting for recording...",
            None,
            session_state,
            None,
            status_text,
            None
        )

    print(f"📊 Auto-analyzing Attempt #{session_state['total_attempts'] + 1}...")
    status_text = "🔬 Analyzing your blow..."
    
    # Trim and Analyze
    trimmed_file = trim_to_blow(audio_filepath)
    features = analyze_audio(trimmed_file)
    report, current_score = evaluate_attempt(features)
    
    print(f"📊 Attempt #{session_state['total_attempts'] + 1} SCORE: {current_score}%")
    
    # Update State
    is_passing = current_score >= PASSING_THRESHOLD
    session_state["total_attempts"] += 1
    session_state["attempts"].append((current_score, is_passing))
    if is_passing:
        session_state["passing_attempts"].append(current_score)
    
    passing_count = len(session_state["passing_attempts"])
    total_count = session_state["total_attempts"]
    graph_img = generate_attempt_graph(session_state["attempts"], session_state["passing_attempts"], session_state["total_attempts"])
    
    # Exit Conditions
    if passing_count >= 3:
        avg_passing = sum(session_state["passing_attempts"]) / passing_count
        session_state["test_complete"] = True
        final_report = f"""
# 🎉 VALID TEST COMPLETE!

You achieved **{passing_count}** passing attempts out of {total_count}.

**Final Valid Score:** **{avg_passing:.0f}%**  
*(Averaged from your {passing_count} acceptable blows.)*

{report}
"""
        status_text = "🏁 Test Complete! Press 'Reset' to start over."
        return (
            gr.update(visible=True),
            f"✅ VALID! Passing: {passing_count}/3 | Final Score: {avg_passing:.0f}%",
            final_report,
            None,
            session_state,
            graph_img,
            status_text,
            None
        )
    
    elif total_count >= MAX_ATTEMPTS:
        session_state["test_complete"] = True
        final_report = f"""
# ❌ Max Attempts Reached

You completed **{total_count}** attempts but only achieved **{passing_count}** passing blows.

**(Need 3 passing attempts for a valid test.)**

{report}
"""
        status_text = "🏁 Max attempts reached. Press 'Reset'."
        return (
            gr.update(visible=True),
            f"❌ Max attempts. Passing: {passing_count}/3",
            final_report,
            None,
            session_state,
            graph_img,
            status_text,
            None
        )
    
    else:
        remaining = MAX_ATTEMPTS - total_count
        need = 3 - passing_count
        status_text = f"✅ Attempt {total_count} done! Score: {current_score}%. Click 'Start Live Test' for the next attempt."
        
        final_report = f"""
### 🔄 Attempt {total_count} / {MAX_ATTEMPTS} Complete

**Passing Attempts So Far:** {passing_count} / 3  
**Remaining Chances:** {remaining}  
**You need {need} more passing blow(s).**

---

{report}
"""
        return (
            gr.update(visible=True),
            f"Attempt {total_count}/{MAX_ATTEMPTS} | Passing: {passing_count}/3 | Need {need} more",
            final_report,
            None,
            session_state,
            graph_img,
            status_text,
            None  # Keep the mic value intact to avoid infinite loops
        )

# --------------------------------------------------
# THERAPIST
# --------------------------------------------------

def request_therapist():
    text = "# 👨‍⚕️ Respiratory Therapist Requested\n\nYour respiratory therapist has now been requested. Please follow your therapist's instructions."
    audio_path = generate_therapist_audio()
    return text, audio_path

# --------------------------------------------------
# RESET + GO BACK
# --------------------------------------------------

def reset_live_session():
    new_state = {
        "attempts": [],
        "passing_attempts": [],
        "total_attempts": 0,
        "test_complete": False
    }
    return ("", "", gr.update(visible=False), None, new_state, "🔄 Session Reset. Click 'Start Live Test' to begin.")

def go_back_to_practicing():
    new_state = {
        "attempts": [],
        "passing_attempts": [],
        "total_attempts": 0,
        "test_complete": False
    }
    return ("", "", gr.update(visible=False), None, new_state, gr.update(selected=2), "📋 Going back to Practice...")

# --------------------------------------------------
# BUILD UI
# --------------------------------------------------

def build_live_assistant(tabs_component):
    welcome_audio_path = generate_welcome_audio()

    session_state = gr.State({
        "attempts": [],
        "passing_attempts": [],
        "total_attempts": 0,
        "test_complete": False
    })

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
            #therapist-btn {
                background-color: #5b9bd5 !important;
                color: white !important;
                border: 2px solid #2a6a9e !important;
                font-weight: bold !important;
                font-size: 18px !important;
                padding: 15px !important;
                border-radius: 12px !important;
            }
            #therapist-btn:hover { background-color: #7fb8e6 !important; transform: scale(1.02); border-color: #1d4f7a !important; }
            #reset-btn {
                background-color: #17a2b8 !important;
                color: white !important;
                border: 2px solid #0f7c8e !important;
                font-weight: bold !important;
                font-size: 16px !important;
                padding: 12px !important;
                border-radius: 12px !important;
            }
            #reset-btn:hover { background-color: #138496 !important; transform: scale(1.02); border-color: #0b5e6b !important; }
            #back-btn {
                background-color: #17a2b8 !important;
                color: white !important;
                border: 2px solid #0f7c8e !important;
                font-weight: bold !important;
                font-size: 16px !important;
                padding: 12px !important;
                border-radius: 12px !important;
            }
            #back-btn:hover { background-color: #138496 !important; transform: scale(1.02); border-color: #0b5e6b !important; }
            .coach-btn {
                background-color: #28a745 !important;
                color: white !important;
                border-color: #1e7e34 !important;
                font-size: 20px !important;
                padding: 15px !important;
            }
            .coach-btn:hover { background-color: #218838 !important; transform: scale(1.02); }
            .status-box {
                border: 2px solid #007bff !important;
                border-radius: 10px !important;
                padding: 10px !important;
                background-color: #f0f8ff !important;
            }
        </style>
        """)

        gr.Markdown("# 🎯 Live AI Companion (V31)")
        if welcome_audio_path:
            gr.Audio(value=welcome_audio_path, label="🔊 Welcome Message", visible=True, interactive=False, autoplay=True)
        else:
            gr.Markdown("*(Welcome audio could not be generated.)*")

        # --- STATUS BOX (Tells the user exactly what to do) ---
        status_box = gr.Markdown(
            value="🟢 **Ready.** Click **'Start Live Test'** to hear the coach.",
            elem_classes="status-box"
        )

        # --- ROW 1: Therapist ---
        with gr.Row():
            therapist_btn = gr.Button("👨‍⚕️ Request Respiratory Therapist", variant="secondary", scale=2, elem_id="therapist-btn")
        with gr.Row():
            therapist_box = gr.Markdown(value="", scale=2)
            therapist_audio = gr.Audio(label="🔊 Therapist Audio", visible=True, interactive=False, autoplay=True, scale=1)

        # --- ROW 2: Start Coach Button (GREEN) ---
        with gr.Row():
            start_btn = gr.Button(
                "▶ Start Live Test", 
                variant="primary", 
                scale=1,
                elem_classes="coach-btn"
            )

        # --- ROW 3: Attempt History ---
        feedback_box = gr.Markdown(value="")
        attempt_graph = gr.Image(label="📊 Attempt History", visible=True)

        # --- ROW 4: Record Button (ORANGE) ---
        with gr.Row():
            mic_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Click ONCE to RECORD, Click AGAIN to STOP & SCORE",
                format="wav",
                scale=2,
                elem_classes="big-mic"
            )

        # --- ROW 5: Coach Voice Output & Coaching Text ---
        with gr.Row():
            audio_output = gr.Audio(label="🔊 Coach Voice", visible=True, interactive=False, autoplay=True)
        coach_box = gr.Markdown(value="", height=300)

        # --- ROW 6: Reset & Go Back ---
        with gr.Row():
            reset_btn = gr.Button("🔄 Reset Live Session", variant="secondary", scale=1, elem_id="reset-btn")
            back_btn = gr.Button("📋 Go Back to Practicing", variant="secondary", scale=1, elem_id="back-btn")

        finish_btn = gr.Button(visible=False)

    # -----------------------------------------
    # BINDINGS
    # -----------------------------------------

    # Therapist
    therapist_btn.click(fn=request_therapist, inputs=[], outputs=[therapist_box, therapist_audio])

    # Step 1: Coach Button (Streams text + plays audio, updates status)
    start_btn.click(
        fn=play_coach_sequence,
        inputs=[],
        outputs=[coach_box, audio_output, status_box]
    )

    # Step 2: Auto-Analyze when recording stops (on change)
    # Outputs: reset_btn, feedback_box, coach_box, audio_output, session_state, attempt_graph, status_box, mic_input (keep)
    mic_input.change(
        fn=analyze_my_blow,
        inputs=[mic_input, session_state],
        outputs=[
            reset_btn,       # 0
            feedback_box,    # 1
            coach_box,       # 2
            audio_output,    # 3
            session_state,   # 4
            attempt_graph,   # 5
            status_box,      # 6
            mic_input        # 7 (DO NOT CLEAR, prevents loops)
        ]
    )

    # Reset
    reset_btn.click(
        fn=reset_live_session,
        inputs=[],
        outputs=[
            coach_box,
            feedback_box,
            reset_btn,
            attempt_graph,
            session_state,
            status_box
        ]
    )

    # Go Back
    back_btn.click(
        fn=go_back_to_practicing,
        inputs=[],
        outputs=[
            coach_box,
            feedback_box,
            reset_btn,
            attempt_graph,
            session_state,
            tabs_component,
            status_box
        ]
    )

    # Return (compatible with app_v31.py)
    return start_btn, therapist_btn, finish_btn