import pygame
import sys
import Mainski

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Ultimate Card Game")

# Colors and Fonts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 36)


def start_game_action(suits_key):
    Mainski.start_game(suits_key)
    print(f"The game has begun! Please pick cards now.")


def pick_card_action():
    # Just directly call Main.pick_card if it doesn't need arguments
    card = Mainski.pick_card()
    print(f"Picked card: {card}")  # For example, printing picked card to console


buttons = {
    'start_game_1': {
        'color': GREEN,
        'rect': pygame.Rect(200, 59, 500, 76),
        'text': 'Start Game with Traditional Suits',
        'action': lambda: start_game_action(1)  # Pass 1 for traditional suits
    },
    'start_game_2': {
        'color': GREEN,
        'rect': pygame.Rect(200, 150, 500, 76),
        'text': 'Start Game with Emoji Suits',
        'action': lambda: start_game_action(2)  # Pass 2 for Emoji 1 suits
    },
    'start_game_3': {
        'color': GREEN,
        'rect': pygame.Rect(200, 250, 500, 76),
        'text': 'Start Game with another set of Emoji Suits',
        'action': lambda: start_game_action(3)  # Pass 3 for Emoji 2 suits
    },
    'pick_card': {
        'color': GREEN,
        'rect': pygame.Rect(200, 350, 500, 76),
        'text': 'Pick a Card',
        'action': pick_card_action  # No argument needed, directly reference the function
    },
    # ... any other buttons
}

# Helper function to draw text
def draw_text(text, position, color=WHITE):
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)


def draw_buttons():
    for button in buttons.values():
        pygame.draw.rect(screen, button['color'], button['rect'])
        draw_text(button['text'], button['rect'].center)


def handle_button_click(mouse_pos):
    for button_key, button_props in buttons.items():
        if button_props['rect'].collidepoint(mouse_pos):
            button_props['action']()

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    draw_buttons()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_button_click(event.pos)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
