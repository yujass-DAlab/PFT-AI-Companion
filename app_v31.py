"""
=========================================================
PFT AI Companion V31
app_v31.py

Author: Jasmine Yu, ChatGPT, DeepSeek

Purpose:
Main application for the V31 version with enhanced session tracking,
progress indicators, and patient-friendly tooltips.
=========================================================
"""
import gradio as gr

from pages.background_v2  import build_background
from pages.proclamation_v2  import build_proclamation
from pages.spirometry_v31 import build_spirometry
from pages.live_assistant_v31 import build_live_assistant

with gr.Blocks(title="PFT Companion AI V31") as demo:

    with gr.Tabs() as tabs:
        
        # ======== TAB 0: Background ========
        with gr.Tab("Background", id=0) as tab0:
            next_btn = build_background()
            next_btn.click(
                fn=lambda: gr.update(selected=1),
                inputs=[],
                outputs=[tabs]
            )

        # ======== TAB 1: Choose Experience ========
        with gr.Tab("Choose Experience", id=1) as tab1:
            practice_btn, live_btn = build_proclamation()
            practice_btn.click(
                fn=lambda: gr.update(selected=2),
                inputs=[],
                outputs=[tabs]
            )
            live_btn.click(
                fn=lambda: gr.update(selected=3),
                inputs=[],
                outputs=[tabs]
            )

        # ======== TAB 2: Practice Mode (V31) ========
        with gr.Tab("Practice Mode V31", id=2) as tab2:
            reset_btn, go_live_btn = build_spirometry()
            go_live_btn.click(
                fn=lambda: gr.update(selected=3),
                inputs=[],
                outputs=[tabs]
            )

        # ======== TAB 3: Live AI Companion (V31) ========
        with gr.Tab("Live AI Companion V31", id=3) as tab3:            
            start_live_btn, therapist_btn, finish_btn = build_live_assistant(tabs)
            # Connect the "Go to Practice" button to switch to tab 2
            practice_btn.click(
                fn=lambda: gr.update(selected=2),
                inputs=[],
                outputs=[tabs]
            )

demo.launch(server_name="0.0.0.0", server_port=7862)