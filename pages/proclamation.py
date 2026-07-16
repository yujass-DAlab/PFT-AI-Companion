"""
=========================================================
PFT AI Companion
proclamation.py

Author: Jasmine Yu, ChatGPT, DeepSeek
=========================================================
"""
import gradio as gr

def build_proclamation():
    with gr.Column():
        gr.Markdown(
            """
            # Welcome to the PFT AI Companion
            
            ## Choose Your Experience
            
            ### 🫁 Start Training
            **Practice the breathing maneuver** as many times as you need.
            The AI will provide coaching and feedback after every attempt.
            
            ### 🎯 Skip to Real Test
            **Proceed directly to the live test.**  
            The AI will guide you through the same steps, but the results will be saved as your official test attempt.
            """
        )

        with gr.Row():
            practice_btn = gr.Button("🫁 Start Training", variant="primary", scale=3)
            live_btn = gr.Button("🎯 Skip to Real Test", variant="secondary", scale=1)

        gr.Markdown("---")
        gr.Markdown(
            """
            ⚠️ **Disclaimer:** Educational purposes only. Not for diagnosis.
            """
        )

    return practice_btn, live_btn