import os
import numpy as np
from PIL import Image
from block_colors_data import block_colors  # Import block colors dictionary

# Constants
block_folder = 'minecraft_blocks'
input_image_folder = r'C:\Users\davin\OneDrive\Desktop\minecraft_pixel_art\input_images'  # Folder containing input images
input_image_path = r'C:\Users\davin\OneDrive\Desktop\minecraft_pixel_art\input_images\davina.jpg'  # Path to your input image

def calculate_average_color(image):
    # Convert image to RGB mode to ensure only RGB values are present
    image_rgb = image.convert('RGB')
    image_array = np.array(image_rgb)
    average_color = np.mean(image_array, axis=(0, 1))
    red, green, blue = map(int, average_color)  # Extract RGB components and convert to integers
    return red, green, blue  # Return RGB tuple

def generate_pixel_art(input_image, block_colors):
    # Open the input image
    input_image = Image.open(input_image)

    # Calculate the grid size based on the dimensions of the input image
    image_width, image_height = input_image.size
    grid_size = (image_width // 16, image_height // 16)

    # Resize input image to fit the calculated grid size exactly
    input_image = input_image.resize((grid_size[0] * 16, grid_size[1] * 16))

    # Initialize an empty canvas to store the pixel art
    pixel_art = Image.new('RGB', (image_width, image_height))

    # Iterate through each grid cell
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            # Crop the current grid cell from the input image
            left = x * 16
            upper = y * 16
            right = left + 16
            lower = upper + 16
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
    generate_pixel_art(input_image_path, block_colors)
