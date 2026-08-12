"""
=========================================================
Spirometry V4 – PWA Edition with Full Coaching Text
Fixed: No redundant preload, optimised delays, fast speech
Author: Jasmine Yu, ChatGPT, DeepSeek
=========================================================
"""
print("🔍 Starting PWA version...")

import time
import os
import io
import tempfile
import json
from fastapi import FastAPI, Response

print("🔍 Imports started...")

try:
    import gradio as gr
    import numpy as np
    import pandas as pd
    from gtts import gTTS
    from scipy.io import wavfile
    from scipy.signal import hilbert
    import plotly.express as px
    import plotly.graph_objects as go
    print("✅ All libraries imported.")
except Exception as e:
    print(f"❌ Import error: {e}")
    exit()

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

MIN_DURATION = 6.0
MIN_EXPLOSION = 0.30
MIN_STABILITY = 0.70
MAX_ATTEMPTS = 8
LIVE_PASS_THRESHOLD = 80
LIVE_PASS_MILESTONE = 3

# --------------------------------------------------
# COACHING SEQUENCE – optimised delays (slow speech, no cut-off)
# --------------------------------------------------

COACH_SEQUENCE = [
    (1.2, "🧘 Relax", "Relax."),
    (1.2, "Get Ready", "Get ready."),
    (1.8, "Take a deep breath in", "Take a deep breath in."),
    (1.5, "3", "Three. Deeper"),
    (1.5, "2", "Two. Deeper"),
    (3.0, "1", "One. Deeper. Click Record now!"),
    (2.5, "💨 BLAST out!", "Blast out fast and hard!"),
    (1.5, "Keep Going", "Keep going."),
    (1.5, "Keep Going", "Keep going."),
    (1.5, "Keep Going", "Keep going."),
    (1.2, "Don't Stop", "Don't stop."),
    (1.2, "Almost There", "Almost there."),
    (1.2, "Finish", "Finish."),
]

# --------------------------------------------------
# PRE‑LOAD STEP AUDIO FILES (from TTS text = third element)
# --------------------------------------------------

def speak(text, filename=None):
    """Generate a TTS audio file – slow=Fast for speed."""
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        if filename is None:
            filename = f"coach_step_{hash(text)}.mp3"
        else:
            filename = f"coach_step_{filename}.mp3"
        path = os.path.join(tempfile.gettempdir(), filename)
        with open(path, "wb") as f:
            f.write(fp.read())
        return path
    except Exception as e:
        print(f"⚠️ speak error: {e}")
        return None

# We no longer need the preloaded concatenated audio – remove it
PRELOADED_AUDIO = None   # or just don't use it

STEP_AUDIO_PATHS = []
def preload_step_audios():
    global STEP_AUDIO_PATHS
    for idx, (_, _, tts_text) in enumerate(COACH_SEQUENCE):
        path = speak(tts_text, filename=str(idx))
        STEP_AUDIO_PATHS.append(path)
    print("✅ Step audio files preloaded (fast speech).")

preload_step_audios()

# --------------------------------------------------
# AUDIO ENGINE & FEATURE EXTRACTION (unchanged)
# --------------------------------------------------

class AudioEngine:
    @staticmethod
    def extract_features(filepath):
        if filepath is None or not os.path.exists(filepath):
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
                data /= np.max(np.abs(data))
            envelope = np.abs(hilbert(data))
            duration = len(data) / sr
            threshold = 0.02
            onset_candidates = np.where(envelope > threshold)[0]
            if len(onset_candidates) > 0:
                onset = onset_candidates[0]
                onset = max(0, onset - int(0.05 * sr))
            else:
                onset = 0
            window = int(0.4 * sr)
            explosion_window = envelope[onset:onset + window]
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
            return {
                "explosion": round(float(explosion), 3),
                "duration": round(float(duration), 2),
                "stability": round(float(stability), 3)
            }
        except Exception as e:
            print(f"❌ AudioEngine error: {e}")
            return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}

# --------------------------------------------------
# SCORING (unchanged)
# --------------------------------------------------

def analyze_audio(filepath):
    if filepath is None or not os.path.exists(filepath):
        return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}
    return AudioEngine.extract_features(filepath)

def evaluate_attempt(features):
    blast = min(features["explosion"] / MIN_EXPLOSION, 1.0) * 100
    duration = min(features["duration"] / MIN_DURATION, 1.0) * 100
    stability = min(features["stability"] / MIN_STABILITY, 1.0) * 100
    total = round(blast * 0.50 + duration * 0.30 + stability * 0.20)
    weakest = min(blast, duration, stability)
    if weakest == blast:
        advice = "🔹 Your Explosive Start needs work. Try a sharp cough-like burst."
    elif weakest == duration:
        advice = "🔹 Your Duration needs work. Exhale steadily for 6 seconds."
    else:
        advice = "🔹 Your Consistency is dropping. Keep a steady airflow."
    if total >= 95:
        stars = "⭐⭐⭐⭐⭐"
        msg = "Outstanding!"
    elif total >= 90:
        stars = "⭐⭐⭐⭐"
        msg = "Excellent!"
    elif total >= 80:
        stars = "⭐⭐⭐"
        msg = "Good effort!"
    else:
        stars = "⭐⭐"
        msg = "Keep practicing."
    report = f"""
### Performance
Explosive Start: **{blast:.0f}%**
Duration: **{duration:.0f}%**
Consistency: **{stability:.0f}%**
## {stars}
{msg}
{advice}
Overall Score: **{total}%**
"""
    return report, total, blast, duration, stability

# --------------------------------------------------
# ATTEMPT HISTORY (unchanged)
# --------------------------------------------------

attempt_history = []
live_session = {"total_attempts": 0, "attempts": []}

def log_attempt(score, mode, blast, duration, stability):
    attempt_history.append((score, mode, blast, duration, stability))

def get_unified_chart():
    if not attempt_history:
        fig = go.Figure()
        fig.update_layout(height=180, yaxis=dict(range=[0,100], dtick=20, title="Score (%)"),
                          xaxis=dict(range=[0.5,8.5], tickvals=list(range(1,9)), ticktext=[str(i) for i in range(1,9)]),
                          plot_bgcolor="#F8F9FA", paper_bgcolor="#F8F9FA", margin=dict(l=30,r=20,t=20,b=30))
        return fig
    scores = [s[0] for s in attempt_history]
    modes = [s[1] for s in attempt_history]
    labels = [f"{i+1} ({'P' if m=='practice' else 'L'})" for i, m in enumerate(modes)]
    df = pd.DataFrame({"Attempt": labels, "Score": scores, "Mode": modes})
    fig = px.bar(df, x="Attempt", y="Score", text="Score", color="Mode",
                 color_discrete_map={"practice": "#f39c12", "live": "#8e44ad"})
    fig.update_traces(textposition="outside", width=0.45)
    fig.update_layout(height=180, yaxis=dict(range=[0,100], dtick=20, title="Score (%)", gridcolor="#e9ecef"),
                      plot_bgcolor="#F8F9FA", paper_bgcolor="#F8F9FA", margin=dict(l=30,r=20,t=20,b=30),
                      showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.add_hline(y=80, line_dash="dash", line_color="#2ecc71", annotation_text="Pass", annotation_position="top right")
    return fig

def get_attempt_summary():
    if not attempt_history:
        return "No attempts yet."
    total = len(attempt_history)
    practice = sum(1 for s, m, _, _, _ in attempt_history if m == "practice")
    live = total - practice
    passing = sum(1 for s, _, _, _, _ in attempt_history if s >= 80)
    return f"""
**Attempt Summary:**  
- **Total:** {total}  
- **Practice:** {practice} | **Live:** {live}  
- **Passing (≥80%):** {passing} | **Failing (<80%):** {total-passing}
    """

def get_detailed_summary():
    if not attempt_history:
        return "No attempts yet."
    scores = [s[0] for s in attempt_history]
    blasts = [s[2] for s in attempt_history]
    durations = [s[3] for s in attempt_history]
    stabilities = [s[4] for s in attempt_history]
    avg = np.mean(scores)
    if avg >= 95: stars = "⭐⭐⭐⭐⭐"
    elif avg >= 90: stars = "⭐⭐⭐⭐☆"
    elif avg >= 80: stars = "⭐⭐⭐☆☆"
    elif avg >= 70: stars = "⭐⭐☆☆☆"
    else: stars = "⭐☆☆☆☆"
    weakest = min(np.mean(blasts), np.mean(durations), np.mean(stabilities))
    if weakest == np.mean(blasts):
        focus = "Explosive Start"
        tip = "Try a sharp burst."
    elif weakest == np.mean(durations):
        focus = "Duration"
        tip = "Hold your exhale longer."
    else:
        focus = "Consistency"
        tip = "Keep steady airflow."
    return f"""
### Detailed Summary
**Stars:** {stars}
Focus on: **{focus}** – {tip}
**Averages:** Blast: {np.mean(blasts):.1f}% | Duration: {np.mean(durations):.1f}% | Stability: {np.mean(stabilities):.1f}%
    """

def get_trend_list():
    if not attempt_history:
        return "No attempts yet."
    lines = []
    for i, (score, mode, _, _, _) in enumerate(attempt_history, 1):
        mode_label = "(P)" if mode == "practice" else "(L)"
        if i == 1:
            lines.append(f"{i}. {mode_label} **{score}%**")
        else:
            prev = attempt_history[i-2][0]
            arrow = "(UP)" if score > prev else ("(DOWN)" if score < prev else "(SAME)")
            lines.append(f"{i}. {mode_label} **{score}%** {arrow}")
    return "\n".join(lines)

def get_score_gauge_html(score):
    if score >= 90: emoji, label = "🟢", "Excellent"
    elif score >= 80: emoji, label = "🟡", "Good"
    else: emoji, label = "🔴", "Keep Practicing"
    return f'<div class="score-gauge" style="background:#000000; color:#ffffff; padding:12px 16px; border-radius:16px; font-size:40px; font-weight:bold; text-align:center; height:82px; min-height:82px; box-sizing:border-box; display:flex; align-items:center; justify-content:center;">{emoji} {score}% – {label}</div>'

def get_coaching_html(text):
    text_br = text.replace("\n", "<br>")
    return f'<div style="background:#1a1a2e; color:#ffffff; padding:16px; border-radius:12px; font-size:18px; line-height:1.6; height:300px; overflow-y:auto;">{text_br}</div>'

# --------------------------------------------------
# MODE + COACHING CONTROL – no preloaded audio
# --------------------------------------------------

CURRENT_MODE = "practice"
COACHING_ID = 0

def run_coaching(mode):
    global CURRENT_MODE, COACHING_ID
    CURRENT_MODE = mode
    COACHING_ID += 1
    my_coaching_id = COACHING_ID
    status = "🟠 **Practice Mode**" if mode == "practice" else "🟣 **Live Mode**"
    text = f"{status}\n\n### 🎧 Listen to the coach...\n\n"
    # No preloaded audio – just start with the first step
    for idx, (delay, _, tts_text) in enumerate(COACH_SEQUENCE):
        if my_coaching_id != COACHING_ID:
            return
        text += f"**{tts_text}**\n\n"
        audio_path = STEP_AUDIO_PATHS[idx]
        yield status, get_coaching_html(text), audio_path
        elapsed = 0.0
        while elapsed < delay:
            time.sleep(0.1)
            elapsed += 0.1
            if my_coaching_id != COACHING_ID:
                return
    if my_coaching_id == COACHING_ID:
        text += "\n✅ Coaching finished. Click Record to capture your blow!"
        yield status, get_coaching_html(text), None

def on_practice():
    yield from run_coaching("practice")

def on_live():
    yield from run_coaching("live")

# --------------------------------------------------
# THERAPIST (fast, unchanged)
# --------------------------------------------------

def request_therapist():
    try:
        tts = gTTS(text="A respiratory therapist has been notified. Someone will assist you shortly.", lang="en", slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        path = os.path.join(tempfile.gettempdir(), "therapist.mp3")
        with open(path, "wb") as f:
            f.write(fp.read())
        audio_path = path
    except Exception as e:
        print(f"❌ Therapist audio error: {e}")
        audio_path = None
    return audio_path, """
# 👨‍⚕️ Respiratory Therapist Requested
Your respiratory therapist has been notified. Someone will assist you shortly.
Please follow your therapist's instructions.
"""

# --------------------------------------------------
# RECORDING ANALYSIS (unchanged)
# --------------------------------------------------

def analyze_recording(filepath):
    current_mode = CURRENT_MODE
    global attempt_history, live_session
    if filepath is None or not os.path.exists(filepath):
        return get_coaching_html("No recording."), get_score_gauge_html(0), get_unified_chart(), get_attempt_summary(), "**Live Attempts:** 0 / 8", gr.update(visible=False), gr.update(), get_detailed_summary(), get_trend_list(), None
    try:
        features = analyze_audio(filepath)
        report, score, blast, duration, stability = evaluate_attempt(features)
    except Exception as e:
        return get_coaching_html(f"Error: {str(e)}"), get_score_gauge_html(0), get_unified_chart(), get_attempt_summary(), "**Live Attempts:** 0 / 8", gr.update(visible=False), gr.update(), get_detailed_summary(), get_trend_list(), None
    log_attempt(score, current_mode, blast, duration, stability)
    if current_mode == "live":
        live_session["total_attempts"] += 1
        live_session["attempts"].append(score)
        total = live_session["total_attempts"]
        passing_live = sum(1 for s in live_session["attempts"] if s >= LIVE_PASS_THRESHOLD)

        counter = f"**Live Attempts:** {total} / {MAX_ATTEMPTS}"
        if passing_live >= LIVE_PASS_MILESTONE:
            counter += (
                f"\n\n"
                f"🟢 **{LIVE_PASS_MILESTONE} passing Live attempts achieved.** "
                "You may finish the session to review your results, or continue practicing."
            )

        reset_visible = gr.update(visible=True) if total >= MAX_ATTEMPTS else gr.update(visible=False)
    else:
        counter = f"**Practice Attempts:** {len(attempt_history)}"
        reset_visible = gr.update(visible=False)
    return (get_coaching_html(report), get_score_gauge_html(score), get_unified_chart(), get_attempt_summary(), counter, reset_visible, gr.update(), get_detailed_summary(), get_trend_list(), None)

def reset_live():
    global live_session
    live_session = {"total_attempts": 0, "attempts": []}
    return get_coaching_html("Reset."), get_score_gauge_html(0), get_unified_chart(), get_attempt_summary(), "**Live Attempts:** 0 / 8", gr.update(visible=False), gr.update(), get_detailed_summary(), get_trend_list(), None

def clear_all_history():
    global attempt_history, live_session
    attempt_history = []
    live_session = {"total_attempts": 0, "attempts": []}
    return get_coaching_html("Cleared."), get_score_gauge_html(0), get_unified_chart(), "No attempts yet.", "**Live Attempts:** 0 / 8", gr.update(visible=False), gr.update(), "No attempts yet.", "No attempts yet.", None

def finish_session():
    return """
# 🎉 Session Complete
Excellent effort. Thank you for practicing with AI Spirometry Companion.
"""

# --------------------------------------------------
# PWA – MANIFEST & SERVICE WORKER (embedded)
# --------------------------------------------------

MANIFEST_JSON = {
    "name": "AI Spirometry Companion",
    "short_name": "Spirometry",
    "description": "Practice PFT maneuvers with AI coaching.",
    "id": "/",
    "display": "standalone",
    "background_color": "#F8F9FA",
    "theme_color": "#1a1a2e",
    "icons": [
        {
            "src": "/static/img/pwa-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any"
        },
        {
            "src": "/static/img/pwa-192.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any"
        }
    ]
}

SW_JS = """
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('spirometry-v3-shell').then(cache => {
            return cache.addAll([
                '/',
                '/favicon.ico'
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
"""

HEAD_HTML = f"""
<link rel="manifest" href="/manifest.json">
<script>
if ('serviceWorker' in navigator) {{
    navigator.serviceWorker.register('/sw.js', {{ scope: '/' }})
        .then(reg => console.log('✅ Service worker registered', reg))
        .catch(err => console.warn('❌ SW registration failed', err));
}}
</script>
"""

# --------------------------------------------------
# BUILD UI (unchanged)
# --------------------------------------------------

def build_spirometry():
    gr.HTML("""
    <style>
        .main-title { font-size: 44px !important; font-weight: bold !important; text-align: center !important; margin-bottom: 20px !important; }
        .dashboard-group { background: #EEF2F6 !important; border-radius: 16px !important; padding: 20px !important; margin-top: 16px !important; border: 1px solid #D8E0E8 !important; }
        .tracker-card { background: #F8F9FA !important; border-radius: 16px !important; padding: 20px !important; margin-top: 16px !important; border: 1px solid #D9DEE5 !important; }
        .status-tag {
            font-size: 32px !important;
            font-weight: bold !important;
            padding: 10px !important;
            border-radius: 12px !important;
            text-align: center !important;
            height: 82px !important;
            min-height: 82px !important;
            box-sizing: border-box !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: #000000 !important;
            color: #ffffff !important;
        }
        /* Keep the three status controls visually aligned, but never clip the native recorder. */
        .audio-wrap {
            height: auto !important;
            min-height: 96px !important;
            overflow: visible !important;
        }
        .audio-wrap .record-button {
            min-height: 82px !important;
            height: auto !important;
            font-size: 24px !important;
        }
        .score-gauge {
            height: 82px !important;
            min-height: 82px !important;
        }
        .rtr-row {
            align-items: stretch !important;
            gap: 12px !important;
            margin-top: 8px !important;
            margin-bottom: 12px !important;
        }
        /* RTR text + audio: matched, harmonious panels */
        .rtr-row .rtr-response,
        .rtr-row .rtr-audio {
            height: 110px !important;
            min-height: 110px !important;
            box-sizing: border-box !important;
        }
        .rtr-row .rtr-response {
            display: flex !important;
            align-items: center !important;
        }
        .rtr-row .rtr-audio {
            background: #F8F9FA !important;
            border: 1px solid #D9DEE5 !important;
            border-radius: 12px !important;
            padding: 0 !important;
            overflow: hidden !important;
        }
        .rtr-row .rtr-audio > div {
            background: #F8F9FA !important;
            border-radius: 12px !important;
        }
        /* RTR response: force readable dark text regardless of Gradio Markdown inheritance */
        .rtr-response, .rtr-response * {
            color: #263238 !important;
        }
        .rtr-response {
            background: #F8F9FA !important;
            border: 1px solid #D9DEE5 !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            font-size: 20px !important;
            line-height: 1.45 !important;
        }
        .rtr-audio audio {
            background: #F8F9FA !important;
        }
        /* Live Session Tracker: explicit contrast against the light tile */
        .tracker-card, .tracker-card * {
            color: #263238 !important;
        }
        .tracker-card {
            background: #F8F9FA !important;
        }
        /* Performance Dashboard report text: match the proven readable dark charcoal */
        .dashboard-group .attempt-summary,
        .dashboard-group .attempt-summary *,
        .dashboard-group .detail-summary,
        .dashboard-group .detail-summary *,
        .dashboard-group .trend-list,
        .dashboard-group .trend-list * {
            color: #263238 !important;
        }
        .dashboard-group .attempt-summary,
        .dashboard-group .detail-summary,
        .dashboard-group .trend-list {
            font-size: 17px !important;
            line-height: 1.5 !important;
        }
        /* How-to-Use step 3: keep the clear X explicitly red */
        .how-to-clear-x {
            color: #d32f2f !important;
            font-weight: 900 !important;
        }
        /* Make Record audio clear X red; keep it in Gradio's native upper-right position */
        .audio-wrap button[aria-label*="Clear"],
        .audio-wrap button[title*="Clear"],
        .audio-wrap button[aria-label*="clear"],
        .audio-wrap button[title*="clear"] {
            color: #d32f2f !important;
        }
        .audio-wrap button[aria-label*="Clear"] svg,
        .audio-wrap button[title*="Clear"] svg,
        .audio-wrap button[aria-label*="clear"] svg,
        .audio-wrap button[title*="clear"] svg {
            color: #d32f2f !important;
            fill: #d32f2f !important;
            stroke: #d32f2f !important;
        }
        #therapist-btn { background-color: #3498db !important; color: white !important; border: 2px solid #2980b9 !important; font-weight: bold !important; }
        #practice-btn { background-color: #f39c12 !important; color: white !important; border: 2px solid #d68910 !important; font-weight: bold !important; }
        #live-btn { background-color: #8e44ad !important; color: white !important; border: 2px solid #6c3483 !important; font-weight: bold !important; }
        #finish-btn { background-color: #1abc9c !important; color: white !important; border: 2px solid #16a085 !important; font-weight: bold !important; }
        #reset-btn { background-color: #f1c40f !important; color: black !important; border: 2px solid #d4ac0d !important; font-weight: bold !important; }
        #clear-history-btn { background-color: #e67e22 !important; color: white !important; border: 2px solid #d35400 !important; font-weight: bold !important; }
        .accordion-fix .accordion { border: none !important; box-shadow: none !important; }
        .accordion-fix .accordion-header { background: #f8f9fa !important; border-left: 6px solid #3498db !important; }
    </style>
    """)

    with gr.Column():
        gr.Markdown('<div class="main-title">AI Spirometry PWA Companion (V4 🫁)</div>\n**One page. Two modes. All stats.**')

        with gr.Accordion("📖 About This App", open=False, elem_classes="accordion-fix"):
            with gr.Accordion("📘 Background Information", open=False):
                gr.Markdown("**Welcome!** Feeling nervous? You're not alone. This app helps you practice PFT maneuvers.")
            with gr.Accordion("⚡ FEV₁", open=False):
                gr.Markdown("FEV₁ is the amount of air you can blow out in the first second of a forceful exhalation.")
            with gr.Accordion("💨 FVC", open=False):
                gr.Markdown("FVC is the total amount of air you can forcefully exhale after a deep breath.")
            with gr.Accordion("🫁 PFT", open=False):
                gr.Markdown("Pulmonary Function Test – a group of tests that evaluate overall lung function.")
            with gr.Accordion("⭐ Before You Begin", open=False):
                gr.Markdown("""
                - ✔ Listen carefully to the instructions.
                - ✔ Take your time between attempts.
                - ✔ If you become dizzy, rest.
                - ✔ Multiple attempts are normal.
                - ✔ The goal is **not perfection**—it's getting reliable measurements.
                """)

        mode_status = gr.Markdown(value="🟠 Practice Mode", elem_classes="status-tag")

        with gr.Row():
            therapist_btn = gr.Button("👨‍⚕️ Request Respiratory Therapist", scale=2, elem_id="therapist-btn")
        with gr.Row(elem_classes="rtr-row"):
            therapist_box = gr.Markdown(elem_classes="rtr-response", scale=1)
            therapist_audio = gr.Audio(
                visible=True,
                interactive=False,
                autoplay=True,
                elem_classes="rtr-audio",
                scale=1,
                waveform_options={
                    "waveform_color": "#3498DB",
                    "waveform_progress_color": "#2980B9"
                }
            )

        with gr.Row():
            practice_btn = gr.Button("🟠 Practice Mode", scale=2, elem_id="practice-btn")
            live_btn = gr.Button("🟣 Live AI Companion", scale=2, elem_id="live-btn")

        with gr.Row(equal_height=True):
            with gr.Column(scale=1, min_width=280):
                gr.Markdown("""
### 📋 How to Use
1. Choose a mode above.
2. Click Record to start (click again to stop).
3. <span class="how-to-clear-x">✖</span> Clear Audio to reset.
                """)
            with gr.Column(scale=2, min_width=420):
                mic_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Click RECORD to start (click STOP to score)", format="wav", scale=3, elem_classes="audio-wrap")

        with gr.Accordion("📝 Coaching & Results", open=True):
            coach_audio = gr.Audio(visible=True, interactive=False, autoplay=True)
            coach_box = gr.HTML(value="", height=300)

        with gr.Column(elem_classes="dashboard-group"):
            gr.HTML('<h2 style="color:#000000; margin-top:0;">📊 Performance Dashboard</h2>')
            gr.HTML('<h3 style="color:#000000;">📊 Instant Effort Score</h3>')
            score_gauge = gr.HTML(value=get_score_gauge_html(0))
            gr.HTML('<h3 style="color:#000000;">📈 Unified Attempt Progress</h3>')
            attempt_summary = gr.Markdown(value="No attempts yet.", elem_classes="attempt-summary")
            attempt_chart = gr.Plot(value=get_unified_chart())
            gr.HTML('<h3 style="color:#000000;">📊 Detailed Summary & Trend</h3>')
            with gr.Row():
                detailed_summary_box = gr.Markdown(value="No attempts yet.", scale=1, elem_classes="detail-summary")
                trend_list_box = gr.Markdown(value="No attempts yet.", scale=1, elem_classes="trend-list")

        with gr.Column(elem_classes="tracker-card"):
            gr.Markdown("### 📊 Live Session Tracker")
            attempt_counter = gr.Markdown(value="**Live Attempts:** 0 / 8")
            with gr.Row():
                reset_btn = gr.Button("🔄 Reset Live Session", visible=False, elem_id="reset-btn")
                clear_history_btn = gr.Button("🗑️ Clear All History", visible=True, elem_id="clear-history-btn")

        gr.Markdown("---")
        with gr.Row():
            finish_btn = gr.Button("🔷 Finish Session", scale=2, elem_id="finish-btn")
        finish_box = gr.Markdown()
        gr.Markdown("⚠️ Disclaimer: Educational purposes only. Not a substitute for clinical judgment.")

    # Events
    therapist_btn.click(fn=request_therapist, inputs=[], outputs=[therapist_audio, therapist_box])
    finish_btn.click(fn=finish_session, outputs=finish_box)

    practice_btn.click(
        fn=on_practice,
        inputs=[],
        outputs=[mode_status, coach_box, coach_audio]
    )
    live_btn.click(
        fn=on_live,
        inputs=[],
        outputs=[mode_status, coach_box, coach_audio]
    )

    mic_input.change(fn=analyze_recording, inputs=[mic_input], outputs=[
        coach_box, score_gauge, attempt_chart, attempt_summary, attempt_counter,
        reset_btn, mic_input, detailed_summary_box, trend_list_box, coach_audio
    ])

    reset_btn.click(fn=reset_live, inputs=[], outputs=[
        coach_box, score_gauge, attempt_chart, attempt_summary, attempt_counter,
        reset_btn, mic_input, detailed_summary_box, trend_list_box, coach_audio
    ])

    clear_history_btn.click(fn=clear_all_history, inputs=[], outputs=[
        coach_box, score_gauge, attempt_chart, attempt_summary, attempt_counter,
        reset_btn, mic_input, detailed_summary_box, trend_list_box, coach_audio
    ])

    return None

# --------------------------------------------------
# LAUNCH – with PWA route injection
# --------------------------------------------------

if __name__ == "__main__":
    print("🟢 Building PWA‑enabled UI with final audio timing...")
    demo = gr.Blocks(title="PFT AI Companion V4")
    with demo:
        build_spirometry()

    app = demo.app

    @app.get("/manifest.json")
    async def manifest():
        return Response(content=json.dumps(MANIFEST_JSON), media_type="application/json")

    @app.get("/sw.js")
    async def service_worker():
        return Response(content=SW_JS, media_type="application/javascript")

    print("🟢 PWA routes added: /manifest.json and /sw.js")
    print("🟢 Launching server on 0.0.0.0:7864 ...")
    demo.launch(server_name="0.0.0.0", server_port=7864, head=HEAD_HTML)
    print("🟢 Running.")