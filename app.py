"""
=========================================================
PFT AI Companion 
app.py

Main Application
Author: Jasmine Yu, ChatGPT, DeepSeek
=========================================================
"""
import gradio as gr

from pages.background import build_background
from pages.proclamation import build_proclamation
from pages.spirometry import build_spirometry
from pages.live_assistant import build_live_assistant

with gr.Blocks(title="PFT Companion AI") as demo:

    # Create tabs with IDs for programmatic switching
    with gr.Tabs() as tabs:
        
        # ======== TAB 0: Background ========
        with gr.Tab("Background", id=0) as tab0:
            next_btn = build_background()
            # When "NEXT" is clicked, switch to tab 1
            next_btn.click(
                fn=lambda: gr.update(selected=1),
                inputs=[],
                outputs=[tabs]
            )

        # ======== TAB 1: Choose Experience ========
        with gr.Tab("Choose Experience", id=1) as tab1:
            practice_btn, live_btn = build_proclamation()
            # When "Start Training" is clicked, switch to tab 2
            practice_btn.click(
                fn=lambda: gr.update(selected=2),
                inputs=[],
                outputs=[tabs]
            )
            # When "Skip to Real Test" is clicked, switch to tab 3
            live_btn.click(
                fn=lambda: gr.update(selected=3),
                inputs=[],
                outputs=[tabs]
            )

        # ======== TAB 2: Practice Mode ========
        with gr.Tab("Practice Mode", id=2) as tab2:
            reset_btn, go_live_btn = build_spirometry()
            # When "Go to Live" is clicked, switch to tab 3
            go_live_btn.click(
                fn=lambda: gr.update(selected=3),
                inputs=[],
                outputs=[tabs]
            )

        # ======== TAB 3: Live AI Companion ========
        with gr.Tab("Live AI Companion", id=3) as tab3:
            build_live_assistant()

demo.launch()