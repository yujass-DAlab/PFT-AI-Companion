"""
======================================================
PFT Prep Coach
Module : Background Information
Author : Jasmine Yu, ChatGPT, DeepSeek
======================================================
"""
import gradio as gr

BACKGROUND_TEXT = """
# 📘 Background Information

## Welcome!

❤️❤️❤️

Feeling a little nervous?

You're not alone. Not too long ago, I experienced my very first Pulmonary Function Test as well. I quickly discovered that the breathing maneuvers were much more demanding and different from normal breathing than I had expected. Many first-time patients feel exactly the same way. That's one of the reasons this AI Companion was created—to help you become more familiar with the procedure, build confidence, and reduce unnecessary anxiety before and during your examination. We'll take it one step at a time.

Pulmonary Function Testing (PFT) is a **non-invasive physiological test** used to evaluate how well your lungs are functioning. It measures the amount of air your lungs can hold, how quickly you can move air in and out of your lungs, and how efficiently oxygen passes from your lungs into your blood. The test itself **does not diagnose a disease**; instead, it provides important information that helps your doctor evaluate your respiratory health.

The entire appointment usually lasts **30–60 minutes**, depending on the number of tests ordered. Because several breathing methods require maximum effort, the test may feel different from your normal breathing. This is completely expected. Most first-time patients require several practice attempts before producing an acceptable result.

To obtain the most accurate results:

• Follow the respiratory therapist's coaching or my instructions carefully.

• Wear comfortable clothing that does not restrict breathing.

• Avoid smoking before the test.

• Avoid heavy meals immediately before the procedure.

• Inform the staff if you recently had chest pain, eye surgery, abdominal surgery, very high or very low blood pressure readings, severe dizziness, or if you become uncomfortable at any time during testing.

Remember:

**You are not expected to perform perfectly on your first attempt.**

The respiratory therapist is there to coach you throughout the procedure on demand and answer any questions you may have.
"""

ABBREVIATIONS = """
# 📖 Common Terms You May Hear

### 🫁 PFT
**Pulmonary Function Test** – A group of breathing tests that evaluate overall lung function.

---

### 🫁 Spirometry
Measures how much air you can breathe in and out and how quickly you can exhale. This part of the examination focuses on how deeply and forcefully you can exhale. My core purpose is to help you become comfortable with this part and making you more prepared.

---

### 💨 FVC
**Forced Vital Capacity** – The total amount of air you can forcefully blast out after taking the deepest breath possible.

---

### ⚡ FEV₁
**Forced Expiratory Volume in One Second** – The amount of air you can blow out during the **first second** of a forceful exhalation.

---

### 📊 FEV₁ / FVC Ratio
A comparison between FEV₁ and FVC. This helps doctors determine whether airflow obstruction may be present.

---

### 🫁 Lung Volumes
Measures the amount of air contained within your lungs during different phases of breathing, including after a normal breath, a deep breath, and after breathing out as completely as possible. These measurements help evaluate how well your lungs expand and whether air is being trapped inside the lungs.

---

### 🌬️ DLCO
**Diffusing Capacity of the Lung for Carbon Monoxide** – Measures how efficiently gases move from the air sacs of your lungs into your bloodstream. Although the test uses a very tiny, safe amount of carbon monoxide for measurement purposes, it helps estimate how effectively oxygen would normally transfer into your blood.

---

### 💊 Bronchodilator
Sometimes your healthcare provider may order breathing tests before and/or after using an inhaled medication to determine how your lungs respond to the medicine and determine the severity of issues in your lungs.
"""

TIPS = """
# 💡 Helpful Tips

✔ Listen carefully to your respiratory therapist or my instructions.

✔ Take your time between attempts.

✔ If you become dizzy, uncomfortable, or need a break, please tell the staff immediately.

✔ Multiple attempts are normal.

✔ The goal is **not perfection**. The goal is obtaining reliable measurements through teamwork between you, your AI Companion, and your respiratory therapist.
"""


def build_background():
    with gr.Column():
        gr.Markdown(BACKGROUND_TEXT)
        gr.Markdown(ABBREVIATIONS)
        gr.Markdown(TIPS)

        next_btn = gr.Button(
            "Continue ➜",
            variant="primary"
        )

    return next_btn