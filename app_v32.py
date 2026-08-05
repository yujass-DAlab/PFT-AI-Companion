"""
=========================================================
PFT AI Companion V32
Unified Spirometry + Live AI (Multi-Tab)
Author: Jasmien Yu, DeepSeek, ChatGPT
=========================================================
"""

import gradio as gr
from pages.spirometry_v31 import build_spirometry  # reuse your existing Practice
from pages.unified_v32 import build_unified_module
from pages.background import build_background  # if you have one
from pages.proclamation import build_proclamation  # if you have one

# --- Build the app ---
with gr.Blocks(title="PFT AI Companion V32") as demo:
    with gr.Tabs():
        # Tab 1: Background
        with gr.Tab("Background"):
            build_background() if 'build_background' in dir() else gr.Markdown("Background page content here.")
        
        # Tab 2: Proclamation
        with gr.Tab("Proclamation"):
            build_proclamation() if 'build_proclamation' in dir() else gr.Markdown("Proclamation page content here.")
        
        # Tab 3: Spirometry Practice (unchanged from V31)
        with gr.Tab("Spirometry Practice"):
            build_spirometry()  # this should exist in your pages folder
        
        # Tab 4: Live AI Companion (the new unified module)
        with gr.Tab("Live AI Companion"):
            build_unified_module()

# --- Launch ---
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7863, theme=gr.themes.Soft())