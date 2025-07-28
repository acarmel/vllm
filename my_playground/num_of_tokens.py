from transformers import AutoTokenizer

# Load the tokenizer for Qwen2
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")

# Load prompts
system_prompt = open("my_playground/system_prompt.txt", "r").read()
user_prompt = open("my_playground/user_prompt.txt", "r").read()

# Count tokens in system and user text
system_tokens = tokenizer.encode(system_prompt, add_special_tokens=False)
user_tokens = tokenizer.encode(user_prompt, add_special_tokens=False)

print(f"System prompt tokens: {len(system_tokens)}")
print(f"User prompt tokens: {len(user_tokens)}")

# Estimate image token count
# Qwen2-VL treats image tokens as special placeholder like "<image>"
image_token_count = 1  # just one token placeholder typically

from PIL import Image
import math


def count_image_tokens(image_path, patch_size=14):
    """
    Estimate number of visual tokens from an image based on patch size.

    Args:
        image_path (str): Path to the image file
        patch_size (int): Size of ViT patch (default 14x14)

    Returns:
        int: Number of visual tokens
    """
    img = Image.open(image_path)
    width, height = img.size

    patches_w = math.ceil(width / patch_size)
    patches_h = math.ceil(height / patch_size)
    num_tokens = patches_w * patches_h

    return num_tokens


# Example usage
image_file = "my_playground/03.png"  # replace with your image path
img_tokens = count_image_tokens(image_file)
print(f"Estimated image token count: {img_tokens}")


total_tokens = len(system_tokens) + len(user_tokens) + image_token_count +img_tokens
print(f"Total estimated tokens: {total_tokens}")