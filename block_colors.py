import os
import numpy as np
from PIL import Image
from block_colors_data import block_colors  # Import block colors dictionary

block_folder = 'minecraft_blocks'

def calculate_average_color(image):
    # Convert image to RGB mode to ensure only RGB values are present
    image_rgb = image.convert('RGB')
    image_array = np.array(image_rgb)
    average_color = np.mean(image_array, axis=(0, 1))

    if image.mode == 'RGBA':
        # If the image has an alpha channel, remove the alpha channel
        image_array = image_array[:, :, :3]

    return tuple(map(int, np.mean(image_array, axis=(0, 1))))  # Return RGB tuple

for filename in os.listdir(block_folder):
    if filename.endswith('.png'):
        block_name = os.path.splitext(filename)[0]
        image_path = os.path.join(block_folder, filename)
        image = Image.open(image_path)
        average_color = calculate_average_color(image)
        block_colors[block_name] = average_color

print(block_colors)  # For testing purposes
