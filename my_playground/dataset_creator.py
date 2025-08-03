import base64
import os
from io import BytesIO
from PIL import Image
from datasets import Dataset


def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


# Load prompts
system_prompt = open("my_playground/system_prompt.txt", "r").read()
user_prompt = open("my_playground/user_prompt.txt", "r").read()

# Get image files
image_dir = "my_playground"
image_files = [f for f in os.listdir(image_dir) if
               f.endswith(".png") and f.startswith("0") and len(f) == 6]

# Prepare data for the dataset
data = {"images": [], "conversation": []}

for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)

    # Load image
    image = Image.open(image_path)
    data["images"].append([image])

    # Encode image to base64
    image_b64 = encode_image(image)

    # Create conversation structure
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}

        # [
        #     {"type": "text", "text": user_prompt},
        #     {
        #         "type": "image_url",
        #         "image_url": {
        #             "url": f"data:image/png;base64,{image_b64}"
        #         }
        #     }
        # ]}
    ]
    data["conversation"].append([messages])

# Create Hugging Face Dataset
dataset = Dataset.from_dict(data)

# You can now print the dataset to see its structure
print(dataset)
dataset.push_to_hub("acarmel/ft1", private=True)

# Example of accessing an element
# print(dataset[0]["image"])
# print(dataset[0]["conversation"])
