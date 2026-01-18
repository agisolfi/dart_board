import pygame


class Button:
    def __init__(self, rect, text, on_click):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.font = pygame.font.SysFont("Arial", 36)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, screen):
        pygame.draw.rect(screen, (70, 70, 70), self.rect)
        label = self.font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)
