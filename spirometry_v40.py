"""
=========================================================
Spirometry V40 – FINAL (Titles as HTML with inline styles)
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
        base_advice = "Outstanding! You passed with flying colors"
    elif total >= 90:
        stars = "⭐⭐⭐⭐"
        base_advice = "Excellent! You certainly met the spirometry standards"
    elif total >= 80:
        stars = "⭐⭐⭐"
        base_advice = "Good effort! You met the passing standards"
    else:
        stars = "⭐⭐"
        base_advice = "Keep practicing. Focus on your weaker areas."

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

def get_attempt_summary_text():
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

# --- CARD STYLE ---
CARD_STYLE = """
background:#ffffff;
color:#222222;
padding:16px;
border-radius:12px;
border:1px solid #d9dee5;
box-shadow:0 2px 6px rgba(0,0,0,.08);
line-height:1.6;
"""

def get_attempt_summary_html():
    text = get_attempt_summary_text()
    text_br = text.replace("\n", "<br>")
    return f'<div style="{CARD_STYLE}">{text_br}</div>'

def get_detailed_summary_text():
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
        if avg_blast < 80:
            advice = f"Your **Explosive Start** needs some love. {tip}"
        else:
            advice = f"Your **Explosive Start** is holding steady. Keep that sharp burst!"
    elif weakest_avg == avg_duration:
        focus = "Duration"
        tip = "Focus on exhaling steadily for at least 6 seconds."
        if avg_duration < 80:
            advice = f"Your **Duration** could be longer. {tip}"
        else:
            advice = f"Your **Duration** is solid – great lung hold!"
    else:
        focus = "Consistency"
        tip = "Keep your airflow steady throughout the entire blow—imagine steady candle pressure."
        if avg_stability < 80:
            advice = f"Your **Consistency** is wobbling. {tip}"
        else:
            advice = f"Your **Consistency** is excellent – your flow is beautifully steady!"

    trend_message = ""
    if len(scores) >= 2:
        last = scores[-1]
        prev = scores[-2]
        diff = last - prev
        if diff > 5:
            trend_message = f"📈 **Improved by {diff:.0f}%** since your last attempt! "
        elif diff < -5:
            trend_message = f"📉 **Dropped by {abs(diff):.0f}%** since your last attempt. "
        else:
            trend_message = f"➡️ **Stable** – your score held steady. "

    if avg_blast >= 80 and avg_duration >= 80 and avg_stability >= 80:
        closing = "🌟 You're doing great across the board. Keep it up!"
    else:
        closing = f"💪 Focus on your **{focus}** and you'll see progress."

    return f"""
### 📊 Detailed Summary

**Overall Star Rating:** {stars}

{trend_message}{advice}

**Averages:**  
- Explosive Start: **{avg_blast:.1f}%**  
- Duration: **{avg_duration:.1f}%**  
- Consistency: **{avg_stability:.1f}%**

{closing}
"""

def get_detailed_summary_html():
    text = get_detailed_summary_text()
    text_br = text.replace("\n", "<br>")
    return f'<div style="{CARD_STYLE}">{text_br}</div>'

def get_trend_list_text():
    if not attempt_history:
        return "No attempts yet."
    lines = []
    for i, (score, mode, blast, dur, stab) in enumerate(attempt_history, 1):
        if i == 1:
            arrow = "(SAME)"
        else:
            prev_score = attempt_history[i-2][0]
            if score > prev_score:
                arrow = "(UP)"
            elif score < prev_score:
                arrow = "(DOWN)"
            else:
                arrow = "(SAME)"
        
        mode_label = "(P)" if mode == "practice" else "(L)"
        lines.append(f"{i}. {mode_label} **{score}%** {arrow}")
    return "\n".join(lines)

def get_trend_list_html():
    text = get_trend_list_text()
    text_br = text.replace("\n", "<br>")
    return f'<div style="{CARD_STYLE}">{text_br}</div>'

def get_score_gauge_html(score):
    if score >= 90:
        emoji = "🟢"
        label = "Excellent"
    elif score >= 70:
        emoji = "🟡"
        label = "Good"
    else:
        emoji = "🔴"
        label = "Keep Practicing"
    return f'<div style="background:#000000; color:#ffffff !important; padding:16px 20px; border-radius:16px; font-size:40px; font-weight:bold; text-align:center; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin:8px 0;">{emoji} {score}% – {label}</div>'

def get_coaching_html(text):
    lines = text.split("\n")
    html_lines = []
    for line in lines:
        if line.strip().startswith("###"):
            content = line.replace("###", "").strip()
            html_lines.append(f"<h3>{content}</h3>")
        elif line.strip().startswith("**") and line.strip().endswith("**"):
            content = line.strip("*")
            html_lines.append(f"<p><strong>{content}</strong></p>")
        elif line.strip() == "":
            html_lines.append("<br>")
        else:
            html_lines.append(f"<p>{line}</p>")
    body = "".join(html_lines)
    return f'<div style="background:#000000; color:#ffffff; padding:16px; border-radius:12px; font-size:18px; line-height:1.6; height:300px; overflow-y:auto;">{body}</div>'

# --------------------------------------------------
# COACHING
# --------------------------------------------------

def run_coaching(mode):
    status = "🟠 **Practice Mode**" if mode == "practice" else "🟣 **Live Mode**"
    full_text = f"{status}\n\n### 🎧 Listen to the coach...\n\n"
    
    for delay, sentence, tts_text in COACH_SEQUENCE:
        speak(tts_text)
        full_text += f"**{sentence}**\n\n"
        time.sleep(delay)
    
    full_text += "\n✅ Coaching finished. Click Record to capture your blow!"
    return mode, status, get_coaching_html(full_text)

# --------------------------------------------------
# LIVE SESSION
# --------------------------------------------------

live_session = {"total_attempts": 0, "attempts": []}

def analyze_recording(audio_filepath, current_mode, status_text):
    global attempt_history, live_session
    if audio_filepath is None or not os.path.exists(audio_filepath):
        return (
            get_coaching_html("⚠️ No recording detected. Click Record and try again."),
            get_score_gauge_html(0),
            gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
            get_attempt_summary_html(),
            "**Attempts:** 0 / 8",
            gr.update(visible=False),
            gr.update(),
            get_detailed_summary_html(),
            get_trend_list_html()
        )
    try:
        features = analyze_audio(audio_filepath)
        report, score, blast, duration, stability = evaluate_attempt(features)
    except Exception as e:
        return (
            get_coaching_html(f"❌ Error analyzing audio: {str(e)}. Please try again."),
            get_score_gauge_html(0),
            gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
            get_attempt_summary_html(),
            "**Attempts:** 0 / 8",
            gr.update(visible=False),
            gr.update(),
            get_detailed_summary_html(),
            get_trend_list_html()
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
    gauge_html = get_score_gauge_html(score)
    report_html = get_coaching_html(report)

    return (
        report_html,
        gauge_html,
        gr.update(value=chart_data),
        get_attempt_summary_html(),
        counter_text,
        reset_visible,
        gr.update(),
        get_detailed_summary_html(),
        get_trend_list_html()
    )

def reset_live():
    global live_session
    live_session = {"total_attempts": 0, "attempts": []}
    return (
        get_coaching_html("🔄 Live session reset."),
        get_score_gauge_html(0),
        gr.update(value=get_unified_chart()),
        get_attempt_summary_html(),
        "**Attempts:** 0 / 8",
        gr.update(visible=False),
        gr.update(),
        get_detailed_summary_html(),
        get_trend_list_html()
    )

def clear_all_history():
    global attempt_history, live_session
    attempt_history = []
    live_session = {"total_attempts": 0, "attempts": []}
    return (
        get_coaching_html("🗑️ All history cleared."),
        get_score_gauge_html(0),
        gr.update(value=pd.DataFrame(columns=["Attempt", "Score"])),
        get_attempt_summary_html(),
        "**Attempts:** 0 / 8",
        gr.update(visible=False),
        gr.update(),
        get_detailed_summary_html(),
        get_trend_list_html()
    )

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
        .main-title { font-size: 44px !important; font-weight: bold !important; text-align: center !important; margin-bottom: 20px !important; }
        
        /* Titles now use inline styles, so we can keep minimal CSS */
        .dashboard-group {
            background: #f5f5f5 !important;  /* Match the default Gradio background */
            border-radius: 16px !important;
            padding: 20px !important;
            margin-top: 16px !important;
            border: none !important;          /* Remove the border for a cleaner look */
            box-shadow: none !important;      /* Remove the shadow */            
        }

        .plot-container svg .bar rect {
            width: 14px !important;
            rx: 4px !important;
            transition: all 0.2s ease !important;
            min-height: 10px !important;
        }
        .plot-container .xaxis .tick text {
            font-size: 16px !important;
            font-weight: bold !important;
        }

        .audio-wrap button.clear-button,
        .audio-wrap button[aria-label="Clear"],
        .audio-wrap .clear svg,
        .audio-wrap .record-actions button svg {
            color: #e74c3c !important;
            fill: #e74c3c !important;
            border-color: #e74c3c !important;
        }

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

        .about-accordion { margin: 16px 0 !important; }
        .about-accordion .accordion {
            border: none !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            margin-bottom: 12px !important;
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
    </style>
    """)

    with gr.Column():
        gr.Markdown("""
        <div class="main-title">AI Spirometry Companion (V40)</div>
        **One page. Two modes. All stats.**
        """)

        with gr.Accordion("📖 About This App", open=False, elem_classes="about-accordion"):
            with gr.Accordion("📘 Background Information", open=False, elem_classes="card-bg"):
                gr.Markdown("**Welcome!** ... (full text)")
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

        mode_status = gr.Markdown(value="🟠 **Practice Mode**", elem_classes="status-tag")

        with gr.Row():
            therapist_btn = gr.Button("👨‍⚕️ Request Respiratory Therapist", scale=2, elem_id="therapist-btn")
        therapist_box = gr.Markdown()

        with gr.Row():
            practice_btn = gr.Button("🟠 Practice Mode", scale=2, elem_id="practice-btn")
            live_btn = gr.Button("🟣 Live AI Companion", scale=2, elem_id="live-btn")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("""
### 📋 How to Use

1. **Choose a mode** above.
2. **Click Record** to start (click again to stop).
3. 🎤 <span style="color:#e74c3c; font-weight:bold;">✖ Clear Audio</span> to reset.
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

        # --- COACHING & RESULTS ---
        with gr.Accordion("📝 Coaching & Results", open=True):
            coach_box = gr.HTML(value=get_coaching_html(""), height=300)

        # --- PERFORMANCE DASHBOARD GROUP ---
        with gr.Column(elem_classes="dashboard-group"):
            # --- TITLES NOW RENDERED AS HTML WITH INLINE STYLES (Guaranteed visible) ---
            gr.HTML('<h2 style="color:#000000; margin-top:0; margin-bottom:16px; font-weight:700; font-size:24px;">📊 Performance Dashboard</h2>')
            
            gr.HTML('<h3 style="color:#000000; margin-top:28px; margin-bottom:14px; font-weight:700; font-size:26px;">📊 Instant Effort Score</h3>')
            score_gauge = gr.HTML(value=get_score_gauge_html(0))

            gr.HTML('<h3 style="color:#000000; margin-top:28px; margin-bottom:14px; font-weight:700; font-size:26px;">📈 Unified Attempt Progress</h3>')
            attempt_summary = gr.HTML(value=get_attempt_summary_html())
            attempt_chart = gr.BarPlot(
                value=pd.DataFrame(columns=["Attempt", "Score"]),
                x="Attempt",
                y="Score",
                title="All Attempts (P=Practice, L=Live)",
                height=300
            )

            gr.HTML('<h3 style="color:#000000; margin-top:28px; margin-bottom:14px; font-weight:700; font-size:26px;">📊 Detailed Summary & Trend</h3>')
            with gr.Row():
                detailed_summary_box = gr.HTML(value=get_detailed_summary_html(), scale=1)
                trend_list_box = gr.HTML(value=get_trend_list_html(), scale=1)

        # --- LIVE SESSION TRACKER ---
        gr.Markdown("---")
        gr.Markdown("### 📊 Live Session Tracker", elem_classes="section-header")
        attempt_counter = gr.Markdown(value="**Attempts:** 0 / 8")
        with gr.Row():
            reset_btn = gr.Button("🔄 Reset Live Session", visible=False, elem_id="reset-btn")
            clear_history_btn = gr.Button("🗑️ Clear All History", visible=True, elem_id="clear-history-btn")

        gr.Markdown("---")
        with gr.Row():
            finish_btn = gr.Button("🔷 Finish Session", scale=2, elem_id="finish-btn")
        finish_box = gr.Markdown()

        gr.Markdown("---")
        gr.Markdown("⚠️ **Disclaimer:** Educational purposes only. Not a substitute for professional clinical judgment.")

    # -----------------------------------------
    # EVENTS
    # -----------------------------------------

    current_mode = gr.State("practice")

    therapist_btn.click(fn=request_therapist, outputs=therapist_box)
    finish_btn.click(fn=finish_session, outputs=finish_box)

    def on_practice():
        mode, status, html_text = run_coaching("practice")
        return mode, status, html_text

    def on_live():
        mode, status, html_text = run_coaching("live")
        return mode, status, html_text

    practice_btn.click(
        fn=on_practice,
        inputs=[],
        outputs=[current_mode, mode_status, coach_box]
    )
    live_btn.click(
        fn=on_live,
        inputs=[],
        outputs=[current_mode, mode_status, coach_box]
    )

    mic_input.change(
        fn=analyze_recording,
        inputs=[mic_input, current_mode, mode_status],
        outputs=[
            coach_box,
            score_gauge,
            attempt_chart,
            attempt_summary,
            attempt_counter,
            reset_btn,
            mic_input,
            detailed_summary_box,
            trend_list_box
        ]
    )

    reset_btn.click(
        fn=reset_live,
        inputs=[],
        outputs=[
            coach_box,
            score_gauge,
            attempt_chart,
            attempt_summary,
            attempt_counter,
            reset_btn,
            mic_input,
            detailed_summary_box,
            trend_list_box
        ]
    )

    clear_history_btn.click(
        fn=clear_all_history,
        inputs=[],
        outputs=[
            coach_box,
            score_gauge,
            attempt_chart,
            attempt_summary,
            attempt_counter,
            reset_btn,
            mic_input,
            detailed_summary_box,
            trend_list_box
        ]
    )

    return None

# --------------------------------------------------
# LAUNCH
# --------------------------------------------------
if __name__ == "__main__":
    print("🟢 8. Entering main block...")
    with gr.Blocks(title="PFT AI Companion V39") as demo:
        print("🟢 9. Building UI...")
        build_spirometry()
    print("🟢 10. UI built, launching now...")
    demo.launch(server_name="0.0.0.0", server_port=7863)
    print("🟢 11. Server should be running.")