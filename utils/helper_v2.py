"""
=========================================================
PFT/Spirometry Prep Coach
helper_v2.py

Author: Jasmine Yu, ChatGPT, DeepSeek

Purpose :
Reusable helper functions shared across the application.

This file keeps the rest of the project clean and
avoids repeating code.
=========================================================
"""

import gradio as gr

# -----------------------------------------------------
# Project Information
# -----------------------------------------------------

APP_NAME = "PFT AI Companion"
VERSION = "Version 2.0"

DISCLAIMER = """
Educational purposes only.

Not a substitute for professional clinical judgment or diagnosis.
"""

# -----------------------------------------------------
# Page Header
# -----------------------------------------------------

def page_header(title, subtitle=None):
    text = f"# {title}\n"
    if subtitle:
        text += f"\n### {subtitle}"
    return gr.Markdown(text)

# -----------------------------------------------------
# Section Title
# -----------------------------------------------------

def section(title):
    return gr.Markdown(f"## {title}")

# -----------------------------------------------------
# Progress Bar (Simplified to "Practices: X")
# -----------------------------------------------------

def progress(attempts):
    """
    Returns a simple text display of the number of practices.
    Removes the confusing MAX_ATTEMPTS logic.
    """
    return f"**Practices:** {attempts}"

# -----------------------------------------------------
# Encouragement Messages
# -----------------------------------------------------

def encouragement(score):
    if score >= 90:
        return "🌟 Outstanding! You are ready for the real test."
    elif score >= 80:
        return "👏 Excellent! Keep practicing to perfect your technique."
    elif score >= 65:
        return "👍 Good attempt! Focus on the specific areas mentioned in the feedback."
    else:
        return "💙 Nice try! Most first-time patients need several attempts. You are building muscle memory."

# -----------------------------------------------------
# Horizontal Divider
# -----------------------------------------------------

def divider():
    return gr.Markdown("---")

# -----------------------------------------------------
# Standard Footer
# -----------------------------------------------------

def footer():
    text = """
---

### Thank you

Thank you for using the

**PFT AI Companion**

Remember

Your respiratory therapist remains your best resource during the actual examination.

Please ask questions whenever you are unsure.
"""
    return gr.Markdown(text)

# -----------------------------------------------------
# Disclaimer
# -----------------------------------------------------

def disclaimer():
    return gr.Markdown(
        f"""
---

### Disclaimer

{DISCLAIMER}
"""
    )

# -----------------------------------------------------
# Blue Button
# -----------------------------------------------------

def blue_button(text):
    return gr.Button(text, variant="primary", scale=3)

# -----------------------------------------------------
# Yellow Button
# -----------------------------------------------------

def yellow_button(text):
    return gr.Button(text, variant="secondary", scale=1)

# -----------------------------------------------------
# Success Badge
# -----------------------------------------------------

def badge(text):
    return gr.Markdown(f"""
## ✅ {text}
""")

# -----------------------------------------------------
# AI Coaching Display
# -----------------------------------------------------

def ai_coaching_display(score, feedback_text):
    return gr.Markdown(
        f"""
### 🤖 AI Coach Feedback

**Score:** {score}/100

{feedback_text}
"""
    )