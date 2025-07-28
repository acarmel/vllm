import asyncio
import base64
import httpx
import json
import time

API_URL = "http://localhost:8888/v1/chat/completions"
API_KEY = "abc"

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Load shared inputs
system_prompt = open("my_playground/system_prompt.txt", "r").read()
user_prompt = open("my_playground/user_prompt.txt", "r").read()
image_b64 = encode_image("my_playground/03.png")

# Pre-constructed message template
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

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Async function to send one request
async def send_request(client, request_id):
    payload = {
        "model": "Qwen/Qwen2-VL-7B-Instruct",
        "messages": messages
    }
    try:
        response = await client.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"[Request {request_id}] ✅ Success")
    except httpx.HTTPError as e:
        print(f"[Request {request_id}] ❌ Error: {e}")


# Main function to send concurrent requests and time the process
async def main(num_requests=1000):
    print(f"Sending {num_requests} requests asynchronously...")
    start = time.perf_counter()

    async with httpx.AsyncClient(timeout=600.0) as client:
        tasks = [send_request(client, i+1) for i in range(num_requests)]
        await asyncio.gather(*tasks)

    end = time.perf_counter()
    duration = end - start
    rps = num_requests / duration
    print("\n--- Summary ---")
    print(f"Total requests: {num_requests}")
    print(f"Total time: {duration:.2f} seconds")
    print(f"Requests/sec: {rps:.2f}")

if __name__ == "__main__":
    asyncio.run(main())