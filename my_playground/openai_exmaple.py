import base64
from openai import OpenAI


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key="abc",
)




system_prompt = open("my_playground/system_prompt.txt", "r").read()
user_prompt = open("my_playground/user_prompt.txt", "r").read()
image_b64 = encode_image("my_playground/03.png")

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": [
        {"type": "text", "text": user_prompt},
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_b64}"
            }
        }
    ]}
]


completion = client.chat.completions.create(
    model="Qwen/Qwen2-VL-7B-Instruct",
    messages=messages,
)

print(completion)
# print(completion.choices[0].message.content)

#
#
# from openai import OpenAI
#
# client = OpenAI()
#
# response = client.responses.create(
#     model="gpt-4.1",
#     input=[
#         {
#             "role": "user",
#             "content": [
#                 { "type": "input_text", "text": "what is in this image?" },
#                 {
#                     "type": "input_image",
#                     "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
#                 }
#             ]
#         }
#     ]
# )
#
# print(response)
