"""
=========================================================
PFT AI Companion V3.2
Author: Jasmine Yu, ChatGPT

Major Improvements
------------------
✓ Cleaner architecture
✓ AudioEngine_v3 integration
✓ Better weighted scoring
✓ Easier future Bluetooth integration
✓ Cleaner state management
✓ AWS ready
=========================================================
"""

import os
import time
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import gradio as gr

from utils.Audio_Engine_v3 import AudioEngine
from utils.report_generator import generate_report


# ==========================================================
# PROJECT INFO
# ==========================================================

APP_TITLE = "🫁 PFT AI Companion"

VERSION = "3.2"

AUTHOR = "Buddy & Jass"


# ==========================================================
# PERFORMANCE TARGETS
# ==========================================================

TARGET_EXPLOSION = 0.65
TARGET_DURATION = 6.0
TARGET_STABILITY = 0.75


# Weighting
BLAST_WEIGHT = 0.50
DURATION_WEIGHT = 0.30
STABILITY_WEIGHT = 0.20


# ==========================================================
# FEEDBACK THRESHOLDS
# ==========================================================

PASS_SCORE = 80

GOOD_SCORE = 70

FAIR_SCORE = 50


# ==========================================================
# ATTEMPT HISTORY
# ==========================================================

MAX_HISTORY = 10


# ==========================================================
# GLOBAL SESSION
# ==========================================================

class SessionState:

    def __init__(self):

        self.reset()

    def reset(self):

        self.current_attempt = 0

        self.attempt_scores = []

        self.feedback_history = []

        self.report_history = []

        self.last_audio = None

        self.last_features = None

        self.last_score = None

        self.practice_mode = True

        self.use_ai_companion = True

        self.request_therapist = False


SESSION = SessionState()


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def clamp(value, low=0.0, high=1.0):
    return max(low, min(value, high))


def percent(value):
    return round(value * 100)


def normalize_metric(value, target):

    return clamp(value / target)


def reset_session():

    SESSION.reset()

    return (
        [],
        pd.DataFrame(columns=["Attempt", "Score"]),
        "Session Reset."
    )


# ==========================================================
# SCORE CALCULATOR
# ==========================================================

def calculate_score(features):

    blast = normalize_metric(
        features["explosion"],
        TARGET_EXPLOSION
    )

    duration = normalize_metric(
        features["duration"],
        TARGET_DURATION
    )

    stability = normalize_metric(
        features["stability"],
        TARGET_STABILITY
    )

    total = (
        blast * BLAST_WEIGHT +
        duration * DURATION_WEIGHT +
        stability * STABILITY_WEIGHT
    )

    total = round(total * 100)

    breakdown = {

        "blast": percent(blast),

        "duration": percent(duration),

        "stability": percent(stability),

        "total": total

    }

    return breakdown


# ==========================================================
# SESSION LOGGER
# ==========================================================

def log_attempt(score, feedback):

    SESSION.current_attempt += 1

    SESSION.attempt_scores.append(score)

    SESSION.feedback_history.append(feedback)

    if len(SESSION.attempt_scores) > MAX_HISTORY:

        SESSION.attempt_scores.pop(0)

        SESSION.feedback_history.pop(0)


# ==========================================================
# HISTORY TABLE
# ==========================================================

def build_history_dataframe():

    rows = []

    for i, score in enumerate(SESSION.attempt_scores):

        rows.append({

            "Attempt": i + 1,

            "Score": score

        })

    return pd.DataFrame(rows)
# ==========================================================
# FEATURE EXTRACTION
# ==========================================================

def analyze_attempt(audio_file):

    if audio_file is None:

        return None, "No recording detected."

    features = AudioEngine.extract_features(audio_file)

    SESSION.last_audio = audio_file

    SESSION.last_features = features

    return features, None


# ==========================================================
# COACHING ENGINE
# ==========================================================

def build_feedback(breakdown):

    messages = []

    score = breakdown["total"]

    # ---------- Explosive Start ----------

    if breakdown["blast"] >= 90:

        messages.append("🚀 Excellent explosive start!")

    elif breakdown["blast"] >= 70:

        messages.append("👍 Good blast. Try to explode just a little faster.")

    else:

        messages.append(
            "⚠️ Blast harder immediately after full inhalation."
        )

    # ---------- Duration ----------

    if breakdown["duration"] >= 95:

        messages.append("🌬️ Excellent exhalation duration.")

    elif breakdown["duration"] >= 75:

        messages.append("👍 Blow a little longer.")

    else:

        messages.append(
            "⚠️ Continue blowing until your lungs feel completely empty."
        )

    # ---------- Stability ----------

    if breakdown["stability"] >= 90:

        messages.append("🎯 Very steady airflow.")

    elif breakdown["stability"] >= 70:

        messages.append("👍 Airflow is fairly steady.")

    else:

        messages.append(
            "⚠️ Try to keep your airflow smooth and continuous."
        )

    # ---------- Overall ----------

    if score >= PASS_SCORE:

        overall = "✅ Excellent effort!"

    elif score >= GOOD_SCORE:

        overall = "🙂 Good effort. Small improvements remain."

    elif score >= FAIR_SCORE:

        overall = "🙂 Nice attempt. Practice again."

    else:

        overall = "💪 Don't worry. Practice makes progress."

    return overall, "\n".join(messages)


# ==========================================================
# SCORE PIPELINE
# ==========================================================

def evaluate_attempt(features):

    breakdown = calculate_score(features)

    overall, details = build_feedback(breakdown)

    report = f"""
## AI Coaching Report

### Overall

{overall}

---

### Explosive Start

{breakdown['blast']}%

---

### Duration

{breakdown['duration']}%

---

### Stability

{breakdown['stability']}%

---

## Total Score

# {breakdown['total']}%

---

### AI Recommendations

{details}
"""

    return report, breakdown["total"]


# ==========================================================
# MAIN ANALYSIS PIPELINE
# ==========================================================

def process_attempt(audio_file):

    features, error = analyze_attempt(audio_file)

    if error:

        return (
            error,
            pd.DataFrame(columns=["Attempt","Score"]),
            None
        )

    report, score = evaluate_attempt(features)

    SESSION.last_score = score

    log_attempt(score, report)

    history = build_history_dataframe()

    return (

        report,

        history,

        score

    )


# ==========================================================
# PRACTICE MODE
# ==========================================================

def practice_mode(audio_file):

    report, history, score = process_attempt(audio_file)

    return (

        report,

        history,

        score

    )


# ==========================================================
# LIVE AI COMPANION
# ==========================================================

def live_ai_mode(audio_file):

    report, history, score = process_attempt(audio_file)

    report += """

---

🤖 AI Companion

Great job.

When you're ready,

take a full deep breath,

seal your lips tightly,

and BLAST immediately.

I'll be here after every attempt.
"""

    return (

        report,

        history,

        score

    )
# ==========================================================
# TREND ANALYSIS
# ==========================================================

def analyze_progress():

    scores = SESSION.attempt_scores

    if len(scores) < 2:

        return "Not enough attempts to determine progress."

    latest = scores[-1]

    previous = scores[-2]

    delta = latest - previous

    if delta >= 15:

        return (
            "📈 Outstanding improvement! "
            "Your latest maneuver is significantly better."
        )

    elif delta >= 5:

        return (
            "👍 Nice improvement. "
            "Keep using the same technique."
        )

    elif delta >= -4:

        return (
            "➡️ Performance is stable. "
            "Let's focus on consistency."
        )

    else:

        return (
            "📉 Slight decline detected. "
            "Take a short rest and try again."
        )


# ==========================================================
# RESPIRATORY THERAPIST MODE
# ==========================================================

def therapist_summary():

    if SESSION.last_features is None:

        return "No maneuver has been analyzed."

    f = SESSION.last_features

    text = f"""
👨‍⚕️ Respiratory Therapist Summary

Explosion
{round(f["explosion"],3)}

Duration
{round(f["duration"],2)} sec

Stability
{round(f["stability"],3)}

Latest Score
{SESSION.last_score}%

Trend

{analyze_progress()}

Recommendation

Review technique if repeated attempts remain below target.
"""

    return text


# ==========================================================
# REQUEST THERAPIST
# ==========================================================

def request_therapist():

    SESSION.request_therapist = True

    return therapist_summary()


# ==========================================================
# PRACTICE HISTORY GRAPH
# ==========================================================

def build_progress_chart():

    if len(SESSION.attempt_scores) == 0:

        return pd.DataFrame({

            "Attempt":[],

            "Score":[]

        })

    return pd.DataFrame({

        "Attempt":

            list(range(

                1,

                len(SESSION.attempt_scores)+1

            )),

        "Score":

            SESSION.attempt_scores

    })


# ==========================================================
# SESSION REPORT
# ==========================================================

def export_session():

    if len(SESSION.attempt_scores)==0:

        return "No completed session."

    average = round(

        np.mean(SESSION.attempt_scores),

        1

    )

    best = max(SESSION.attempt_scores)

    report = f"""
==============================

PFT AI Companion

Session Summary

==============================

Attempts

{len(SESSION.attempt_scores)}

Average Score

{average}%

Best Score

{best}%

Latest Trend

{analyze_progress()}

==============================

Thank you for practicing!

==============================
"""

    return report


# ==========================================================
# AI ENCOURAGEMENT ENGINE
# ==========================================================

def encouragement():

    if len(SESSION.attempt_scores)==0:

        return ""

    score = SESSION.last_score

    if score >= 90:

        return (
            "🌟 Fantastic! "
            "You're performing like someone ready for clinical testing."
        )

    elif score >= 80:

        return (
            "👏 Excellent work! "
            "Just maintain this consistency."
        )

    elif score >= 70:

        return (
            "🙂 You're getting close. "
            "Keep practicing the explosive start."
        )

    elif score >= 50:

        return (
            "💪 Good effort! "
            "Every attempt improves muscle memory."
        )

    else:

        return (
            "❤️ Don't be discouraged. "
            "This is exactly why Practice Mode exists."
        )
# ==========================================================
# MASTER PIPELINE
# ==========================================================

def run_ai_companion(audio_file, mode):

    if mode == "Practice":

        report, history, score = practice_mode(audio_file)

    else:

        report, history, score = live_ai_mode(audio_file)

    chart = build_progress_chart()

    encouragement_text = encouragement()

    report += "\n\n"

    report += encouragement_text

    return (

        report,

        history,

        chart,

        score

    )


# ==========================================================
# THERAPIST CALLBACK
# ==========================================================

def therapist_callback():

    return request_therapist()


# ==========================================================
# EXPORT CALLBACK
# ==========================================================

def export_callback():

    return export_session()


# ==========================================================
# RESET CALLBACK
# ==========================================================

def reset_callback():

    return reset_session()


# ==========================================================
# FUTURE BLUETOOTH PLACEHOLDER
# ==========================================================

def bluetooth_mode():

    """
    Reserved for Bluetooth spirometer.

    Future pipeline

    Bluetooth

        ↓

    Read device

        ↓

    Extract FEV1

    FVC

    Flow

        ↓

    AI Coach

    """

    pass

