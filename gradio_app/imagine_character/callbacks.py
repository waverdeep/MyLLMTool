from utils import util
from utils import configs


chat_client = util.register_openai_api_key(configs.config['OPENAI_API_KEY'])


def imagine(connect_key, model_name, input_prompt):

    if connect_key != configs.config['MY_ACCESS_KEY']:
        return None

    response = chat_client.images.generate(
        model=model_name,
        prompt=input_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url


def start_generate():
    return "프롬프트 생성을 시작합니다..."


def generate_prompt(connect_key, model_name, input_prompt, default_prompt):
    output = ""
    if connect_key != configs.config['MY_ACCESS_KEY']:
        output += "Please check the connect key."
        yield output
        return

    system_prompt = ""
    user_prompt = f"Please create a new English prompt for image generation based on the following description. Express it richly so that the image can be generated effectively based on the description. Only output the prompt.\n{input_prompt}, {default_prompt}"
    stream = chat_client.chat.completions.create(
        model=model_name,
        messages=util.get_conversation(system_prompt, [], user_prompt),
        temperature=0.7,
        stream=True
    )

    output = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            output += chunk.choices[0].delta.content
            yield output

