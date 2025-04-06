import pygame
import numpy as np
from ui import GRID_BG, ACCENT_BLUE, POSITIVE_VALUE, NEGATIVE_VALUE, ZERO_VALUE, TEXT_COLOR

class KernelEditor:
    def __init__(self, size=5, cell_size=50, padding=20):
        self.grid_size = size
        self.cell_size = cell_size
        self.padding = padding
        self.kernel = np.zeros((size, size))
        
        # Set center cell to 1 (identity kernel)
        center = size // 2
        self.kernel[center, center] = 1
    
    def reset(self):
        """Reset to identity kernel"""
        self.kernel = np.zeros((self.grid_size, self.grid_size))
        center = self.grid_size // 2
        self.kernel[center, center] = 1
    
    def set_kernel(self, new_kernel):
        """Set the kernel to a new value"""
        if new_kernel.shape != self.kernel.shape:
            # Resize the kernel if needed
            self.grid_size = new_kernel.shape[0]
            self.kernel = new_kernel.copy()
        else:
            self.kernel = new_kernel.copy()
    
    def get_kernel(self):
        """Get the current kernel"""
        return self.kernel.copy()
    
    def draw(self, surface, x, y, font_medium, title_y_offset=-70):
        """Draw the kernel grid at the specified position"""
        grid_width = self.grid_size * self.cell_size
        grid_height = self.grid_size * self.cell_size
        
        # Draw grid title
        title_text = font_medium.render("Kernel Editor (Click to cycle -5 to 5, Right-click for reverse)", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(x + grid_width // 2, y + title_y_offset))
        surface.blit(title_text, title_rect)
        
        # Draw grid background
        grid_rect = pygame.Rect(x, y, grid_width, grid_height)
        pygame.draw.rect(surface, GRID_BG, grid_rect)
        pygame.draw.rect(surface, ACCENT_BLUE, grid_rect, 2)
        
        # Draw grid cells
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_x = x + col * self.cell_size
                cell_y = y + row * self.cell_size
                
                cell_rect = pygame.Rect(cell_x, cell_y, self.cell_size, self.cell_size)
                
                # Determine cell color based on kernel value
                value = self.kernel[row, col]
                if value > 0:
                    # Positive values: teal with intensity based on value
                    intensity = min(255, int(abs(value) * 50))
                    color = (0, 230 - intensity//2, 180 + intensity//4)
                    # Add glow for higher values
                    if value > 1:
                        glow_rect = cell_rect.inflate(4, 4)
                        pygame.draw.rect(surface, color, glow_rect, 1, border_radius=5)
                elif value < 0:
                    # Negative values: pink with intensity based on value
                    intensity = min(255, int(abs(value) * 50))
                    color = (255, 60 + intensity//4, 100 + intensity//2)
                    # Add glow for higher absolute values
                    if abs(value) > 1:
                        glow_rect = cell_rect.inflate(4, 4)
                        pygame.draw.rect(surface, color, glow_rect, 1, border_radius=5)
                else:
                    # Zero: dark gray
                    color = ZERO_VALUE
                
                pygame.draw.rect(surface, color, cell_rect, border_radius=5)
                pygame.draw.rect(surface, ACCENT_BLUE, cell_rect, 1, border_radius=5)
                
                # Draw value text
                text = font_medium.render(f"{int(value)}", True, TEXT_COLOR)
                text_rect = text.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                surface.blit(text, text_rect)
    
    def handle_click(self, pos, x, y, button=1):
        """Handle mouse click on the kernel grid
        
        Args:
            pos: Mouse position (x, y)
            x, y: Grid position
            button: 1 for left click, 3 for right click
            
        Returns:
            True if the grid was clicked, False otherwise
        """
        grid_width = self.grid_size * self.cell_size
        grid_height = self.grid_size * self.cell_size
        
        grid_rect = pygame.Rect(x, y, grid_width, grid_height)
        
        if grid_rect.collidepoint(pos):
            # Calculate which cell was clicked
            col = (pos[0] - x) // self.cell_size
            row = (pos[1] - y) // self.cell_size
            
            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                # Cycle kernel value from -5 to 5
                current_value = self.kernel[row, col]
                
                if button == 1:  # Left click - cycle forward
                    # Increment by 1, or wrap around from 5 to -5
                    if current_value == 5:
                        self.kernel[row, col] = -5
                    else:
                        self.kernel[row, col] = current_value + 1
                elif button == 3:  # Right click - cycle backward
                    # Decrement by 1, or wrap around from -5 to 5
                    if current_value == -5:
                        self.kernel[row, col] = 5
                    else:
                        self.kernel[row, col] = current_value - 1
                
                return True
        
        return False