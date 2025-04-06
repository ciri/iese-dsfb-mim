import os
import pygame
import numpy as np
from PIL import Image, ImageDraw, ImageOps

def create_test_image(size=(200, 200)):
    """Create a simple test image with a grid pattern"""
    img = Image.new('RGB', size, color=(40, 40, 40))
    
    draw = ImageDraw.Draw(img)
    
    # Grid background
    for i in range(0, size[0], 20):
        draw.line([(i, 0), (i, size[1])], fill=(60, 60, 60), width=1)
        draw.line([(0, i), (size[0], i)], fill=(60, 60, 60), width=1)
    
    # Rectangle
    draw.rectangle([size[0]//5, size[1]//5, 4*size[0]//5, 4*size[1]//5], 
                  fill=(80, 80, 80), outline=(120, 120, 120), width=2)
    
    # Circle
    center_x, center_y = size[0]//2, size[1]//2
    radius = min(size[0], size[1])//3
    draw.ellipse([center_x-radius, center_y-radius, center_x+radius, center_y+radius], 
                fill=(100, 100, 100), outline=(140, 140, 140), width=2)
    
    # X pattern
    draw.line([size[0]//10, size[1]//10, 9*size[0]//10, 9*size[1]//10], fill=(160, 160, 160), width=3)
    draw.line([size[0]//10, 9*size[1]//10, 9*size[0]//10, size[1]//10], fill=(160, 160, 160), width=3)
    
    return img

def create_mario_image(size=(200, 200)):
    """Create a simple Mario-like pixel art image"""
    img = Image.new('RGB', size, color=(135, 206, 235))  # Sky blue background
    
    draw = ImageDraw.Draw(img)
    
    # Define colors
    red = (255, 0, 0)      # Mario's hat/shirt
    skin = (252, 188, 176)  # Mario's skin
    blue = (0, 0, 255)     # Mario's overalls
    brown = (150, 75, 0)   # Mario's hair/mustache
    black = (0, 0, 0)      # Outlines
    white = (255, 255, 255) # Eyes
    yellow = (255, 255, 0)  # Buttons
    green = (0, 156, 0)     # Ground
    
    # Scale factors
    w, h = size
    scale_x = w / 200
    scale_y = h / 200
    
    def scaled_rect(coords):
        return [
            int(coords[0] * scale_x),
            int(coords[1] * scale_y),
            int(coords[2] * scale_x),
            int(coords[3] * scale_y)
        ]
    
    # Draw ground
    draw.rectangle(scaled_rect([0, 160, 200, 200]), fill=green)
    
    # Draw Mario's head (simplified pixel art style)
    # Hat
    draw.rectangle(scaled_rect([70, 50, 130, 70]), fill=red)
    draw.rectangle(scaled_rect([60, 70, 140, 80]), fill=red)
    
    # Face
    draw.rectangle(scaled_rect([70, 80, 130, 110]), fill=skin)
    
    # Hair and mustache
    draw.rectangle(scaled_rect([60, 80, 70, 90]), fill=brown)
    draw.rectangle(scaled_rect([130, 80, 140, 90]), fill=brown)
    draw.rectangle(scaled_rect([80, 100, 120, 105]), fill=brown)
    
    # Eyes
    draw.rectangle(scaled_rect([80, 85, 90, 95]), fill=white)
    draw.rectangle(scaled_rect([110, 85, 120, 95]), fill=white)
    draw.rectangle(scaled_rect([83, 88, 87, 92]), fill=black)
    draw.rectangle(scaled_rect([113, 88, 117, 92]), fill=black)
    
    # Body
    draw.rectangle(scaled_rect([80, 110, 120, 140]), fill=blue)
    draw.rectangle(scaled_rect([70, 110, 80, 130]), fill=red)
    draw.rectangle(scaled_rect([120, 110, 130, 130]), fill=red)
    
    # Arms
    draw.rectangle(scaled_rect([60, 110, 70, 130]), fill=skin)
    draw.rectangle(scaled_rect([130, 110, 140, 130]), fill=skin)
    
    # Legs
    draw.rectangle(scaled_rect([70, 140, 90, 160]), fill=blue)
    draw.rectangle(scaled_rect([110, 140, 130, 160]), fill=blue)
    
    # Feet
    draw.rectangle(scaled_rect([60, 160, 90, 170]), fill=brown)
    draw.rectangle(scaled_rect([110, 160, 140, 170]), fill=brown)
    
    # Buttons
    draw.ellipse(scaled_rect([90, 115, 100, 125]), fill=yellow)
    draw.ellipse(scaled_rect([100, 125, 110, 135]), fill=yellow)
    
    return img

def load_image_from_file():
    """Try to load an image from the current directory"""
    try:
        # Try to find test_image.png first
        if os.path.exists('test_image.png'):
            return Image.open('test_image.png')
        
        # Try to find any image in the current directory
        for file in os.listdir('.'):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                return Image.open(file)
        
        # If no image found, return None
        return None
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def apply_kernel(image, kernel):
    """Apply a kernel to an image"""
    if image is None:
        return None
    
    # Convert image to grayscale for simpler processing
    img = ImageOps.grayscale(image)
    img_array = np.array(img)
    
    # Apply convolution
    height, width = img_array.shape
    k_height, k_width = kernel.shape
    
    # Padding
    pad_h = k_height // 2
    pad_w = k_width // 2
    
    # Create output array
    output = np.zeros_like(img_array, dtype=float)
    
    # Normalize the kernel if it's a blur kernel (sum > 1)
    kernel_sum = np.sum(kernel)
    if kernel_sum > 1:
        normalized_kernel = kernel / kernel_sum
    else:
        normalized_kernel = kernel.copy()
    
    # Apply convolution
    for i in range(pad_h, height - pad_h):
        for j in range(pad_w, width - pad_w):
            # Extract the region of interest
            roi = img_array[i - pad_h:i + pad_h + 1, j - pad_w:j + pad_w + 1]
            
            # Apply normalized kernel
            output[i, j] = np.sum(roi * normalized_kernel)
    
    # Normalize output
    output = np.clip(output, 0, 255).astype(np.uint8)
    
    # Convert back to PIL Image and ensure it's in RGB mode
    return Image.fromarray(output).convert('RGB')

def pil_to_pygame(pil_image, size=None):
    """Convert PIL image to Pygame surface"""
    if pil_image is None:
        return None
    
    # Resize if needed
    if size:
        display_img = pil_image.copy()
        display_img.thumbnail(size)
    else:
        display_img = pil_image
    
    # Ensure the mode is 'RGB' for pygame compatibility
    if display_img.mode != 'RGB':
        display_img = display_img.convert('RGB')
    
    # Convert to pygame surface
    size = display_img.size
    data = display_img.tobytes()
    
    return pygame.image.fromstring(data, size, 'RGB')