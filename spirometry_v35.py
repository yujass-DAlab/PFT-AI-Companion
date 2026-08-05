"""
=========================================================
Spirometry V35 – Fixed How-to Box (Markdown Only)
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

attempt_history = []

def log_attempt(score, mode, blast, duration, stability):
    attempt_history.append((score, mode, blast, duration, stability))

def clear_all_history():
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
    elif avg_score >= 90:
        stars = "⭐⭐⭐⭐☆"
    elif avg_score >= 80:
        stars = "⭐⭐⭐☆☆"
    elif avg_score >= 70:
        stars = "⭐⭐☆☆☆"
    else:
        stars = "⭐☆☆☆☆"

    weakest_avg = min(avg_blast, avg_duration, avg_stability)
    if weakest_avg == avg_blast:
        focus = "Explosive Start"
        tip = "Try a sudden, sharp cough-like burst at the very beginning."
    elif weakest_avg == avg_duration:
        focus = "Duration"
        tip = "Focus on exhaling steadily for at least 6 seconds."
    else:
        focus = "Consistency"
        tip = "Keep your airflow steady throughout the entire blow—imagine steady candle pressure."

    if avg_blast >= 80 and avg_duration >= 80 and avg_stability >= 80:
        advice = "You are performing well across all metrics! Keep it up."
    else:
        advice = f"Focus on improving your **{focus}**. {tip}"

    if len(scores) >= 2:
        last = scores[-1]
        prev = scores[-2]
        trend = "📈 Improving" if last > prev else ("📉 Declining" if last < prev else "➡️ Stable")
    else:
        trend = "⏳ Not enough data"

    return f"""
### 📊 Detailed Summary

**Overall Star Rating:** {stars}  
{advice}

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
    coach_text = ""
    for delay, sentence, tts_text in COACH_SEQUENCE:
        coach_text += sentence + "\n\n"
        speak(tts_text)
        yield "practice", status, coach_text
        time.sleep(delay)
    yield "practice", status, coach_text + "\n✅ Coaching finished."

def stream_live():
    status = "🟣 **Live Mode**"
    coach_text = ""
    for delay, sentence, tts_text in COACH_SEQUENCE:
        coach_text += sentence + "\n\n"
        speak(tts_text)
        yield "live", status, coach_text
        time.sleep(delay)
    yield "live", status, coach_text + "\n✅ Coaching finished."

# --------------------------------------------------
# LIVE SESSION STATE
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
# RESET LIVE
# --------------------------------------------------

def reset_live():
    global live_session
    live_session = {"total_attempts": 0, "attempts": []}
    return (
        "🔄 Live session reset.",
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
# CLEAR ALL HISTORY
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
# BUILD UI (V35 – How-to box fixed with pure Markdown)
# --------------------------------------------------

def build_spirometry():
    gr.HTML("""
    <style>
        .main-title { font-size: 44px !important; font-weight: bold !important; text-align: center !important; }
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
        #clear-history-btn { background-color: #e67e22 !important; color: white !important; border: 2px solid #d35400 !important; font-weight: bold !important; }
        #clear-history-btn:hover { background-color: #d35400 !important; }
        .audio-wrap .wrap { height: auto !important; min-height: 120px !important; }
        .audio-wrap .record-button { height: 80px !important; font-size: 24px !important; }
        .status-tag { font-size: 32px !important; font-weight: bold !important; padding: 10px !important; border-radius: 12px !important; text-align: center !important; }
        .section-header { font-size: 22px !important; font-weight: 600 !important; margin-top: 16px !important; margin-bottom: 8px !important; color: #2c3e50 !important; }

        .about-accordion { margin: 12px 0 !important; }
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
        .card-bg .accordion-header { border-left-color: #2c3e50 !important; }
        .card-fev1 .accordion-header { border-left-color: #e74c3c !important; }
        .card-dlco .accordion-header { border-left-color: #8e44ad !important; }
        .card-fvc .accordion-header { border-left-color: #e67e22 !important; }
        .card-ratio .accordion-header { border-left-color: #1abc9c !important; }
        .card-pft .accordion-header { border-left-color: #2ecc71 !important; }
        .card-tips .accordion-header { border-left-color: #f39c12 !important; }

        .howto-box {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 16px 20px;
            border-left: 6px solid #3498db;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
    </style>
    """)

    with gr.Column():
        # --- TITLE ---
        gr.Markdown("""
        <div class="main-title">AI Spirometry Companion (V35 🫁)</div>
        **One page. Two modes. All stats.**
        """)

        # --- ABOUT SECTION ---
        with gr.Accordion("📖 About This App", open=False, elem_classes="about-accordion"):
            with gr.Accordion("📘 Background Information", open=False, elem_classes="card-bg"):
                gr.Markdown("""
**Welcome!**

Feeling a little nervous? You're not alone...
                """)
            with gr.Accordion("⚡ FEV₁", open=False, elem_classes="card-fev1"):
                gr.Markdown("FEV₁ stands for...")
            with gr.Accordion("🌬️ DLCO", open=False, elem_classes="card-dlco"):
                gr.Markdown("DLCO stands for...")
            with gr.Accordion("💨 FVC", open=False, elem_classes="card-fvc"):
                gr.Markdown("FVC stands for...")
            with gr.Accordion("📊 FEV₁/FVC Ratio", open=False, elem_classes="card-ratio"):
                gr.Markdown("The ratio helps...")
            with gr.Accordion("🫁 PFT", open=False, elem_classes="card-pft"):
                gr.Markdown("PFT stands for...")
            with gr.Accordion("⭐ Before We Begin", open=False, elem_classes="card-tips"):
                gr.Markdown("- ✔ Listen carefully...")

        # --- MODE STATUS ---
        mode_status = gr.Markdown(value="🟠 **Practice Mode**", elem_classes="status-tag")

        # --- THERAPIST ---
        with gr.Row():
            therapist_btn = gr.Button("👨‍⚕️ Request Respiratory Therapist", scale=2, elem_id="therapist-btn")
        therapist_box = gr.Markdown()

        # --- MODE BUTTONS (Parallel) ---
        with gr.Row():
            practice_btn = gr.Button("🟠 Practice Mode", scale=2, elem_id="practice-btn")
            live_btn = gr.Button("🟣 Live AI Companion", scale=2, elem_id="live-btn")

        # --- HOW-TO BOX (Fixed: pure Markdown, no broken HTML) ---
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("""
### 📋 How to Use

1. **Choose a mode** above (Practice or Live).
2. **Click Record** to start (click again to stop).
3. 🎤 **✖ Clear Audio** to reset your recording.
                """)
            with gr.Column(scale=2):
                mic_input = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    label="🎤 Click RECORD to start (click STOP to score)",
                    format="wav",
                    scale=3,
                    elem_classes="audio-wrap"
                )

        # --- COACHING & RESULTS (Collapsible) ---
        with gr.Accordion("📝 Coaching & Results", open=True):
            coach_box = gr.Markdown(value="", height=300)

        # --- INSTANT EFFORT SCORE ---
        gr.Markdown("### 📊 Instant Effort Score", elem_classes="section-header")
        with gr.Row():
            big_score_display = gr.Markdown(value="**0%**", elem_classes="big-score")
        score_slider = gr.Slider(label="Overall Score (%)", minimum=0, maximum=100, step=1, value=0, interactive=False, scale=3)

        # --- UNIFIED ATTEMPT PROGRESS ---
        gr.Markdown("### 📈 Unified Attempt Progress (Practice + Live)", elem_classes="section-header")
        attempt_summary = gr.Markdown(value="No attempts recorded yet.")
        attempt_chart = gr.BarPlot(
            value=pd.DataFrame(columns=["Attempt", "Score"]),
            x="Attempt",
            y="Score",
            title="All Attempts (P=Practice, L=Live)",
            height=300
        )

        # --- DETAILED SUMMARY & TREND ---
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

        # --- FINISH SESSION ---
        gr.Markdown("---")
        with gr.Row():
            finish_btn = gr.Button("🔷 Finish Session", scale=2, elem_id="finish-btn")
        finish_box = gr.Markdown()

        # --- DISCLAIMER ---
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
            coach_box,          # 0: Report
            score_slider,       # 1: Score
            attempt_chart,      # 2: Chart
            attempt_summary,    # 3: Summary text
            attempt_counter,    # 4: Counter
            reset_btn,          # 5: Reset visibility
            mic_input,          # 6: No-op
            detailed_summary_box, # 7: Detailed summary
            trend_list_box,     # 8: Trend list
            big_score_display   # 9: Big score number
        ]
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
    with gr.Blocks(title="PFT AI Companion V35") as demo:
        print("🟢 9. Building UI...")
        build_spirometry()
    print("🟢 10. UI built, launching now...")
    demo.launch(server_name="0.0.0.0", server_port=7863)
    print("🟢 11. Server should be running.")