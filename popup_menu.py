__author__ = "AndyVoyager"

import pygame
from settings import WHITE, BLACK, RED, GREEN, HIGHLIGHTED_GREEN, HIGHLIGHTED_RED

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)


def draw_button(screen, text, x, y, width, height, color, highlight_color, mouse_pos):
    # Change the color of the button if the mouse is hovering over it
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        pygame.draw.rect(screen, highlight_color, (x, y, width, height))
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    # Add the text to the button
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)


def ask_to_play_again(screen):
    screen.fill(BLACK)

    # The main loop
    while True:
        mouse_pos = pygame.mouse.get_pos()  # get the current mouse position

        screen.fill(BLACK)

        # Show the text
        text = font.render("You won! Do you want to play again?", True, WHITE)
        # screen.blit(text, (250, 150))
        text_rect = text.get_rect()
        text_rect.center = (screen.get_width() // 2, 200)
        screen.blit(text, text_rect)

        # Draw the buttons
        draw_button(screen, "Yes", 250, 250, 100, 50, GREEN, HIGHLIGHTED_GREEN, mouse_pos)
        draw_button(screen, "No", 450, 250, 100, 50, RED, HIGHLIGHTED_RED, mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the "Yes" button
                if 250 <= mouse_pos[0] <= 350 and 250 <= mouse_pos[1] <= 300:
                    return True
                # If the user clicked on the "No" button
                elif 450 <= mouse_pos[0] <= 550 and 250 <= mouse_pos[1] <= 300:
                    return False
