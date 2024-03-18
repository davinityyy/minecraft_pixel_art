import os
import numpy as np
from PIL import Image
from block_colors_data import block_colors  # Import block colors dictionary

# Constants
block_folder = 'minecraft_blocks'
input_image_folder = 'input_images'  # Folder containing input images
input_image_path = 'input_image.jpg'  # Path to your input image
grid_size = (10, 10)  # Define the grid size (e.g., 10x10 for Minecraft blocks)

# Load Minecraft block colors dictionary generated from block_colors.py
block_colors = {
    'acacia_leaves': (86, 85, 85),
    'acacia_log': (103, 96, 86),
    # Add all other block colors here
}

def calculate_average_color(image):
    # Convert image to RGB mode to ensure only RGB values are present
    image_rgb = image.convert('RGB')
    image_array = np.array(image_rgb)
    average_color = np.mean(image_array, axis=(0, 1))
    red, green, blue = map(int, average_color)  # Extract RGB components and convert to integers
    return red, green, blue  # Return RGB tuple

def generate_pixel_art(input_image, block_colors, grid_size):
    # Open the input image
    input_image = Image.open(input_image)

    # Resize input image to fit the grid
    input_image = input_image.resize((grid_size[0] * 16, grid_size[1] * 16))  # Assuming Minecraft block size is 16x16 pixels

    # Divide the input image into grid cells
    width, height = input_image.size
    cell_width = width // grid_size[0]
    cell_height = height // grid_size[1]

    # Initialize an empty canvas to store the pixel art
    pixel_art = Image.new('RGB', (width, height))

    # Iterate through each grid cell
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            # Crop the current grid cell from the input image
            left = x * cell_width
            upper = y * cell_height
            right = left + cell_width
            lower = upper + cell_height
            cell_image = input_image.crop((left, upper, right, lower))

            # Calculate the average color of the current grid cell
            average_color = calculate_average_color(cell_image)

            # Find the Minecraft block with the closest average color
            closest_block = min(block_colors.keys(), key=lambda name: np.linalg.norm(np.array(block_colors[name]) - np.array(average_color)))

            # Load the texture of the closest matching block
            block_texture_path = os.path.join(block_folder, f"{closest_block}.png")
            block_texture = Image.open(block_texture_path)

            # Paste the block texture onto the canvas
            pixel_art.paste(block_texture, (x * 16, y * 16))

    # Save the generated pixel art
    pixel_art.save('output_pixel_art.png')

if __name__ == "__main__":
    generate_pixel_art(input_image_path, block_colors, grid_size)
