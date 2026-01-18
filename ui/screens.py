import pygame
from ui.screen_base import Screen
from ui.widgets import Button


class MainMenu(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.SysFont("Arial", 48)
        self.width, self.height = self.screen.get_size()
        self.start_button = Button(
            rect=(400, 300, 200, 60), text="Start Game", on_click=self.start_game
        )

    def start_game(self):
        self._next = GameSelect(self.screen)

    def handle_event(self, event):
        self.start_button.handle_event(event)

    def draw(self):
        self.screen.fill((30, 30, 30))
        title = self.font.render("Darts N' Shit", True, (255, 255, 255))
        self.screen.blit(title, (400, 200))
        self.start_button.draw(self.screen)


class GameSelect(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.SysFont("Arial", 36)

        self.button_301 = Button(
            rect=(400, 300, 200, 60), text="301", on_click=self.move_to_player_select
        )

    def move_to_player_select(self):
        self._next = PlayerSelect(self.screen)

    def handle_event(self, event):
        self.button_301.handle_event(event)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.button_301.draw(self.screen)


class PlayerSelect(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.SysFont("Arial", 36)

        self.button_1 = Button(
            rect=(150, 300, 200, 60),
            text="1 Player",
            on_click=lambda: self.start_301(1),
        )

        self.button_2 = Button(
            rect=(550, 300, 200, 60),
            text="2 Player",
            on_click=lambda: self.start_301(2),
        )

    def start_301(self, player_count):
        from ui.game_screen import GameScreen

        players = []
        for _ in range(player_count):
            players.append({"score": 301})

        self._next = GameScreen(self.screen, players)

    def handle_event(self, event):
        self.button_1.handle_event(event)
        self.button_2.handle_event(event)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.button_1.draw(self.screen)
        self.button_2.draw(self.screen)

class WinScreen(Screen):
    def __init__(self, screen, winner_index):
        super().__init__(screen)
        self.winner = winner_index
        self.font_large = pygame.font.SysFont("Arial", 64)
        self.font_small = pygame.font.SysFont("Arial", 32)

        self.menu_button = Button(
            rect=(400, 400, 300, 60),
            text="Back to Menu",
            on_click=self.back_to_menu
        )

    def back_to_menu(self):
        from ui.screens import MainMenu
        self._next = MainMenu(self.screen)

    def handle_event(self, event):
        self.menu_button.handle_event(event)

    def draw(self):
        self.screen.fill((20, 20, 20))

        text = self.font_large.render(
            f"Player {self.winner + 1} Wins!",
            True,
            (255, 215, 0)
        )
        self.screen.blit(text, text.get_rect(center=(640, 200)))

        self.menu_button.draw(self.screen)
