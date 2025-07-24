import base64
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key="abc",
)



system_prompt = open("my_playground/system_prompt.txt", "r").read()
user_prompt = open("my_playground/user_prompt.txt", "r").read()
image_b64 = base64.b64encode(open("my_playground/01.png", "rb").read()).decode("utf-8")

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": [
        {"type": "text", "text": user_prompt},
        {"type": "image", "image": image_b64}
    ]}
]


completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=messages,
)

