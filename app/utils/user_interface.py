import gradio as gr
from utils.configs import *
from utils.callbacks import *


with gr.Blocks() as config_demo:
    with gr.Row():
        with gr.Column():
            model_dropdown = gr.Dropdown(
                choices=allowed_models,
                value="gpt-3.5-turbo-1106",
                interactive=True,
                label="selet model"
            )
            system_prompt_textbox = gr.Textbox(
                label="system prompt",
            ), 
            temerature_silder = gr.Slider(
                minimum=0, 
                maximum=1, 
                step=0.1,
                value=0.5,
                label="temperature"
            ),
            access_key_textbox = gr.Textbox(
                label="my access key",
                type="password"
            ),


with gr.Blocks() as history_demo:
    with gr.Row():
        with gr.Column(scale=3):
            gr.Label(
                value="Chat History"
            )
        with gr.Column(scale=7):
            history_chatbot = gr.Chatbot(
                show_copy_button=True
            )
            




