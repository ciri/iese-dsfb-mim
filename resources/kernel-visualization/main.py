import pygame
import sys
import numpy as np
from PIL import Image

# Import our modules
from ui import Button, load_fonts, draw_panel, DARK_BG, PANEL_BG, ACCENT_BLUE, TEXT_COLOR
from filters import KernelFilters
from image_utils import create_test_image, create_mario_image, load_image_from_file, apply_kernel, pil_to_pygame
from kernel_editor import KernelEditor

# Constants
WINDOW_WIDTH = 1000
GRID_SIZE = 5  # Default kernel size (5x5) - updated from 3x3
WINDOW_HEIGHT = 700
CELL_SIZE = 50
GRID_MARGIN = 30
IMAGE_DISPLAY_SIZE = (280, 280)
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 140
BUTTON_MARGIN = 15
PANEL_PADDING = 20

class KernelVisualizer:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Create window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Image Kernel Visualizer - (c) Enric Junque de Fortuny 2025")
        
        # Initialize clock
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load fonts
        self.font_large, self.font_medium, self.font_small = load_fonts()
        
        # Create kernel editor
        self.kernel_editor = KernelEditor(GRID_SIZE, CELL_SIZE, PANEL_PADDING)
        
        # Image processing
        self.original_image = None
        self.processed_image = None
        self.original_surface = None
        self.processed_surface = None
        
        # Create buttons
        self.create_buttons()
        
        # Create Mario image by default
        self.create_mario_image()
    
    def create_buttons(self):
        """Create all the buttons for the application"""
        self.buttons = []
        
        # Calculate the bottom panel area
        panel_height = 100
        panel_y = WINDOW_HEIGHT - panel_height
        
        # Create a 2x4 grid of buttons at the bottom
        button_grid_width = (BUTTON_WIDTH * 4) + (BUTTON_MARGIN * 3)
        button_grid_x = (WINDOW_WIDTH - button_grid_width) // 2
        
        # Row 1 (bottom) - First row of kernels
        button_y = panel_y + panel_height - BUTTON_HEIGHT - BUTTON_MARGIN
        
        # Apply Kernel button (for manual edits)
        self.buttons.append(Button(
            button_grid_x,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Apply Kernel",
            self.apply_kernel
        ))
        
        # Reset Kernel button
        self.buttons.append(Button(
            button_grid_x + BUTTON_WIDTH + BUTTON_MARGIN,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Reset Kernel",
            self.reset_kernel_and_apply
        ))
        
        # Edge detection kernels
        self.buttons.append(Button(
            button_grid_x + (BUTTON_WIDTH + BUTTON_MARGIN) * 2,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "All Edges",
            lambda: self.set_kernel_and_apply(KernelFilters.edge_detection())
        ))
        
        self.buttons.append(Button(
            button_grid_x + (BUTTON_WIDTH + BUTTON_MARGIN) * 3,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Left Edge",
            lambda: self.set_kernel_and_apply(KernelFilters.left_edge())
        ))
        
        # Row 2 - More kernels
        button_y -= BUTTON_HEIGHT + BUTTON_MARGIN
        
        self.buttons.append(Button(
            button_grid_x,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Top Edge",
            lambda: self.set_kernel_and_apply(KernelFilters.top_edge())
        ))
        
        self.buttons.append(Button(
            button_grid_x + BUTTON_WIDTH + BUTTON_MARGIN,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Diagonal Edge",
            lambda: self.set_kernel_and_apply(KernelFilters.diagonal_edge())
        ))
        
        self.buttons.append(Button(
            button_grid_x + (BUTTON_WIDTH + BUTTON_MARGIN) * 2,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Box Blur",
            lambda: self.set_kernel_and_apply(KernelFilters.box_blur())
        ))
        
        self.buttons.append(Button(
            button_grid_x + (BUTTON_WIDTH + BUTTON_MARGIN) * 3,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Gaussian Blur",
            lambda: self.set_kernel_and_apply(KernelFilters.gaussian_blur())
        ))
        
        # Row 3 - More filters
        button_y -= BUTTON_HEIGHT + BUTTON_MARGIN
        
        self.buttons.append(Button(
            button_grid_x,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Sharpen",
            lambda: self.set_kernel_and_apply(KernelFilters.sharpen())
        ))
        
        self.buttons.append(Button(
            button_grid_x + BUTTON_WIDTH + BUTTON_MARGIN,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Emboss",
            lambda: self.set_kernel_and_apply(KernelFilters.emboss())
        ))
        
        self.buttons.append(Button(
            button_grid_x + (BUTTON_WIDTH + BUTTON_MARGIN) * 2,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Ring Detect",
            lambda: self.set_kernel_and_apply(KernelFilters.ring_detection())
        ))
        
        self.buttons.append(Button(
            button_grid_x + (BUTTON_WIDTH + BUTTON_MARGIN) * 3,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Motion Blur",
            lambda: self.set_kernel_and_apply(KernelFilters.motion_blur())
        ))
    
    def create_test_image(self):
        """Create a test image"""
        self.original_image = create_test_image()
        self.update_image_display()
        self.apply_kernel()
        return True
    
    def create_mario_image(self):
        """Create a Mario image"""
        self.original_image = create_mario_image()
        self.update_image_display()
        self.apply_kernel()
        return True
    
    def reset_kernel_and_apply(self):
        """Reset kernel to identity and apply"""
        self.kernel_editor.reset()
        self.apply_kernel()
        return True
    
    def set_kernel_and_apply(self, kernel):
        """Set kernel to a new value and apply"""
        self.kernel_editor.set_kernel(kernel)
        self.apply_kernel()
        return True
    
    def update_image_display(self):
        """Update the pygame surfaces from PIL images"""
        if self.original_image:
            self.original_surface = pil_to_pygame(self.original_image, IMAGE_DISPLAY_SIZE)
        
        if self.processed_image:
            self.processed_surface = pil_to_pygame(self.processed_image, IMAGE_DISPLAY_SIZE)
    
    def apply_kernel(self):
        """Apply the current kernel to the original image"""
        if not self.original_image:
            return False
        
        # Get the current kernel
        kernel = self.kernel_editor.get_kernel()
        
        # Apply the kernel to the image
        self.processed_image = apply_kernel(self.original_image, kernel)
        
        # Update the display
        self.update_image_display()
        
        return True
    
    def draw_images(self):
        """Draw the original and processed images"""
        # Calculate the vertical center position
        vertical_center = WINDOW_HEIGHT // 2 - 20  # Slight adjustment for buttons at bottom
        
        # Draw original image (left side)
        if self.original_surface:
            # Calculate position - left side
            image_width = self.original_surface.get_width()
            image_height = self.original_surface.get_height()
            image_x = WINDOW_WIDTH // 6 - image_width // 2
            image_y = vertical_center - image_height // 2
            
            # Draw panel background
            panel_width = image_width + PANEL_PADDING * 2
            panel_height = image_height + PANEL_PADDING * 2 + 30
            panel_x = image_x - PANEL_PADDING
            panel_y = image_y - PANEL_PADDING - 30
            
            # Draw panel with title
            draw_panel(self.screen, panel_x, panel_y, panel_width, panel_height, 
                      "Original", self.font_medium)
            
            # Draw image
            self.screen.blit(self.original_surface, (image_x, image_y))
        
        # Draw processed image (right side)
        if self.processed_surface:
            # Calculate position - right side
            image_width = self.processed_surface.get_width()
            image_height = self.processed_surface.get_height()
            image_x = 5 * WINDOW_WIDTH // 6 - image_width // 2
            image_y = vertical_center - image_height // 2
            
            # Draw panel background
            panel_width = image_width + PANEL_PADDING * 2
            panel_height = image_height + PANEL_PADDING * 2 + 30
            panel_x = image_x - PANEL_PADDING
            panel_y = image_y - PANEL_PADDING - 30
            
            # Draw panel with title
            draw_panel(self.screen, panel_x, panel_y, panel_width, panel_height, 
                      "Processed", self.font_medium)
            
            # Draw image
            self.screen.blit(self.processed_surface, (image_x, image_y))
    
    def run(self):
        """Main application loop"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEMOTION:
                    # Update button hover states
                    for button in self.buttons:
                        button.check_hover(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle mouse clicks
                    if event.button == 1 or event.button == 3:  # Left or right click
                        # Calculate kernel grid position
                        grid_width = self.kernel_editor.grid_size * self.kernel_editor.cell_size
                        grid_height = self.kernel_editor.grid_size * self.kernel_editor.cell_size
                        grid_x = (WINDOW_WIDTH - grid_width) // 2
                        grid_y = (WINDOW_HEIGHT - grid_height) // 2 - 20
                        
                        # Handle kernel grid clicks
                        grid_clicked = self.kernel_editor.handle_click(event.pos, grid_x, grid_y, event.button)
                        
                        # Handle button clicks only if grid wasn't clicked
                        if not grid_clicked and event.button == 1:
                            for button in self.buttons:
                                button.handle_event(event)
            
            # Fill background
            self.screen.fill(DARK_BG)
            
            # Draw app title with copyright
            title_text = self.font_large.render("IMAGE KERNEL VISUALIZER", True, TEXT_COLOR)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 25))
            self.screen.blit(title_text, title_rect)
            
            # Draw bottom panel for buttons
            panel_height = 100
            panel_y = WINDOW_HEIGHT - panel_height
            panel_rect = pygame.Rect(0, panel_y, WINDOW_WIDTH, panel_height)
            pygame.draw.rect(self.screen, PANEL_BG, panel_rect)
            pygame.draw.line(self.screen, ACCENT_BLUE, (0, panel_y), (WINDOW_WIDTH, panel_y), 2)
            
            # Draw images
            self.draw_images()
            
            # Draw kernel grid
            grid_width = self.kernel_editor.grid_size * self.kernel_editor.cell_size
            grid_height = self.kernel_editor.grid_size * self.kernel_editor.cell_size
            grid_x = (WINDOW_WIDTH - grid_width) // 2
            grid_y = (WINDOW_HEIGHT - grid_height) // 2 - 20
            
            # Draw kernel editor
            self.kernel_editor.draw(self.screen, grid_x, grid_y, self.font_medium, title_y_offset=-50)
            
            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen, self.font_medium)
            
            # Update display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = KernelVisualizer()
    app.run()