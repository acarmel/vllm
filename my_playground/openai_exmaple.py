from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key="abc",
)


completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[
        {"role": "developer", "content": "Talk like a pirate."},
        {
            "role": "user",
            "content": "How do I check if a Python object is an instance of a class?",
        },
    ],
)

