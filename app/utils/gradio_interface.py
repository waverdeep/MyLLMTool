import time
import gradio as gr

import utils.util as util
from utils.configs import *


chat_client = util.register_openai_api_key(config['OPENAI_API_KEY'])


def predict(message, history, model_name, system_prompt, temperature, access_key, chat_id):
    global chat_client
    global allowed_models
    global config

    if chat_id == "":
        yield "Please click 'Start Chat' button."
        return

    if "gpt" in model_name and chat_client is None:
        yield "Please register the openai api key."
        return

    if model_name not in allowed_models:
        yield "Please select the model again."
        return

    if access_key != config['MY_ACCESS_KEY']:
        yield "Please check the my access key."
        return

    stream = chat_client.chat.completions.create(
        model=model_name,
        messages= util.get_conversation(system_prompt, history, message),
        temperature=temperature,
        stream=True
    )

    partial_message = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message

chat_id_hidden = gr.Textbox(
    value="",
    label="chat_id",
    interactive=False
)


chat = gr.ChatInterface(
    predict,
    chatbot=gr.Chatbot(height="60vh"),
    textbox=gr.Textbox(
        placeholder="무엇이든 물어보세요!", 
        container=False, 
        scale=7
    ),
    stop_btn=None,
    additional_inputs_accordion_name="configurations",
    additional_inputs=[
        gr.Dropdown(
            choices=allowed_models,
            value="gpt-3.5-turbo-1106",
            interactive=True,
            label="selet model"
        ),
        gr.Textbox(
            "", 
            label="system prompt"), 
        gr.Slider(
            minimum=0, 
            maximum=1, 
            step=0.1,
            value=0.5,
            label="temperature"),
        gr.Textbox(
            label="my access key",
            type="password"
        ),
        chat_id_hidden
    ],
).queue()


with gr.Blocks(theme="soft", title="MLT",) as demo:
    with gr.Row():
        with gr.Group():
            start_button = gr.Button(
                value="Start Chat"
            )
            chat_id_textbox = gr.Textbox(
                value="",
                label="chat id",
                interactive=False
            )
            start_button.click(
                util.create_chat_id,
                inputs=[],
                outputs=[chat_id_textbox]
            )
    with gr.Row():
        with gr.Column(scale=7):
            chat.render()
        with gr.Column(scale=3):
            with gr.Group():
                gr.Label(
                    value="Additional Tools"
                )
                title_textbox = gr.Textbox(
                    label="chat title",
                    placeholder="제목을 꼭 입력해주세요 (나중엔 자동화할 것!)"
                )
                save_button = gr.Button(
                    value="Save chat history",
                )
                result_dataframe = gr.DataFrame(
                    headers=["id", "title"],
                    datatype=["number", "str"],
                    value=[[time.time(), "what's up!"]],
                    type="pandas",
                    interactive=False
                )
                save_button.click(
                    util.save_button_event,
                    inputs=[chat.chatbot, title_textbox, result_dataframe],
                    outputs=[result_dataframe, title_textbox, chat.chatbot]
                )
                

