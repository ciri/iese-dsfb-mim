# Image Kernel Visualizer

A modular Python application that allows you to visualize and experiment with image kernels (convolution matrices) and see their effects on images in real-time.

## Features

- Interactive kernel editor: Click to cycle values from -5 to 5, right-click to cycle in reverse
- Multiple preset kernels: Edge detection, blur, sharpen, emboss, and more
- Real-time visualization of kernel effects on images
- Modern sci-fi themed interface
- Modular code structure for easy maintenance and extension

## Requirements

- Python 3.6+
- Pygame
- Pillow (PIL)
- NumPy

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main application:

```bash
python main.py
```

## Project Structure

The project is organized into modular components:

- `main.py` - Main application file
- `ui.py` - UI components and styling
- `filters.py` - Collection of kernel filters
- `image_utils.py` - Image loading and processing utilities
- `kernel_editor.py` - Kernel grid editor functionality

## How to Use

1. **Edit the Kernel**: Click on cells in the grid to cycle values from -5 to 5. Right-click to cycle in the opposite direction.
2. **Apply the Kernel**: Click the "Apply Kernel" button to apply your manual edits to the image.
3. **Try Preset Kernels**: Use the preset buttons to try common kernels like Edge Detection, Blur, etc.
4. **View Results**: See the original image on the left and the processed image on the right.

## Understanding Kernels

Image kernels (or convolution matrices) are small matrices used for image processing operations like blurring, sharpening, edge detection, and more. The kernel is applied to each pixel in the image by centering it on the pixel and multiplying each kernel value with the corresponding pixel value, then summing the results.

## License

© Enric Junque de Fortuny 2025