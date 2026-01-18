import pygame
from ui.screens import MainMenu

pygame.init()
screen = pygame.display.set_mode((1024, 600))
pygame.display.set_caption("Smart Dartboard")

clock = pygame.time.Clock()
current_screen = MainMenu(screen)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_screen.handle_event(event)

    current_screen.update()
    current_screen.draw()
    next_screen = current_screen.next_screen()
    if next_screen:
        current_screen = next_screen            
    pygame.display.flip()

pygame.quit()
