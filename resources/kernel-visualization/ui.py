import pygame

# Colors - Sci-fi theme
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BG = (15, 20, 30)  # Dark blue-black background
PANEL_BG = (25, 30, 40)  # Slightly lighter for panels
GRID_BG = (35, 40, 50)   # Grid background
ACCENT_BLUE = (0, 150, 255)  # Bright blue for highlights
ACCENT_CYAN = (0, 210, 230)  # Cyan for secondary highlights
POSITIVE_VALUE = (0, 230, 180)  # Teal for positive values
NEGATIVE_VALUE = (255, 60, 100)  # Pink for negative values
ZERO_VALUE = (50, 55, 65)  # Dark gray for zero values
TEXT_COLOR = (220, 230, 240)  # Light blue-white for text
BUTTON_IDLE = (40, 45, 60)  # Button background
BUTTON_HOVER = (60, 70, 90)  # Button hover state

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, surface, font):
        color = BUTTON_HOVER if self.hovered else BUTTON_IDLE
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, ACCENT_BLUE, self.rect, 2, border_radius=10)
        
        # Glow effect when hovered
        if self.hovered:
            glow_rect = self.rect.inflate(4, 4)
            pygame.draw.rect(surface, ACCENT_CYAN, glow_rect, 1, border_radius=12)
        
        text_surface = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            if self.action:
                return self.action()
        return False

def load_fonts():
    """Load and return fonts for the application"""
    try:
        font_large = pygame.font.Font(None, 36)
        font_medium = pygame.font.Font(None, 28)
        font_small = pygame.font.Font(None, 22)
    except:
        font_large = pygame.font.SysFont(None, 36)
        font_medium = pygame.font.SysFont(None, 28)
        font_small = pygame.font.SysFont(None, 22)
    
    return font_large, font_medium, font_small

def draw_panel(surface, x, y, width, height, title=None, font=None):
    """Draw a panel with optional title"""
    panel_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, PANEL_BG, panel_rect, border_radius=10)
    pygame.draw.rect(surface, ACCENT_BLUE, panel_rect, 2, border_radius=10)
    
    if title and font:
        title_text = font.render(title, True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(x + width // 2, y + 15))
        surface.blit(title_text, title_rect)
        
    # Draw corner accents
    corner_size = 10
    pygame.draw.line(surface, ACCENT_CYAN, 
                    (x + 5, y + 5), 
                    (x + 5 + corner_size, y + 5), 2)
    pygame.draw.line(surface, ACCENT_CYAN, 
                    (x + 5, y + 5), 
                    (x + 5, y + 5 + corner_size), 2)
    
    pygame.draw.line(surface, ACCENT_CYAN, 
                    (x + width - 5, y + 5), 
                    (x + width - 5 - corner_size, y + 5), 2)
    pygame.draw.line(surface, ACCENT_CYAN, 
                    (x + width - 5, y + 5), 
                    (x + width - 5, y + 5 + corner_size), 2)