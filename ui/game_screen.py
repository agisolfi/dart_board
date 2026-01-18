import pygame
from ui.screen_base import Screen
from ui.widgets import Button
import math

DART_NUMBERS = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

SLICE_COLORS = [(20, 20, 20), (230, 230, 230)]  # black  # white

RED = (200, 0, 0)
GREEN = (0, 160, 0)


class GameScreen(Screen):
    def __init__(self, screen, players):
        super().__init__(screen)
        self.players = players
        self.current_player = 0
        self.last_throw = None
        self.font_large = pygame.font.SysFont("Arial", 36)
        self.font_small = pygame.font.SysFont("Arial", 24)
        self.impacts = []  # list of (x, y)
        self.width, self.height = self.screen.get_size()
        self.board_center = (self.width * 0.4, self.height * 0.5)
        self.board_radius = int(min(self.width, self.height) * 0.4)

        self.next_button = Button(
            rect=(724, 500, 200, 50), text="Next Player", on_click=self.next_player
        )

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)
        self.last_throw = None

    def draw_wedge(self, start_angle, end_angle, inner_r, outer_r, color):
        cx, cy = self.board_center
        points = []

        # Outer arc
        steps = 20
        for i in range(steps + 1):
            a = start_angle + (end_angle - start_angle) * i / steps
            x = cx + math.cos(a) * outer_r
            y = cy + math.sin(a) * outer_r
            points.append((x, y))

        # Inner arc (reverse)
        for i in range(steps + 1):
            a = end_angle - (end_angle - start_angle) * i / steps
            x = cx + math.cos(a) * inner_r
            y = cy + math.sin(a) * inner_r
            points.append((x, y))

        pygame.draw.polygon(self.screen, color, points)

    def draw_ring(self, radius_frac, color, width=0):
        r = int(self.board_radius * radius_frac)
        pygame.draw.circle(self.screen, color, self.board_center, r, width)

    def handle_event(self, event):
        self.next_button.handle_event(event)

        # TEMP: simulate dart with spacebar
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.simulate_throw()

    def simulate_throw(self):
        import random
        from ui.screens import WinScreen

        x = random.uniform(-0.95, 0.95)
        y = random.uniform(-0.95, 0.95)

        self.impacts.append((x, y))

        result = self.score_from_xy(x, y)
        if result:
            score, mult = result
            self.last_throw = (score, mult)
            self.players[self.current_player]["score"] -= score * mult

        if self.players[self.current_player]["score"] <= 0:
            self._next = WinScreen(self.screen, self.current_player)

    def score_from_xy(self, x, y):
        r = math.sqrt(x * x + y * y)

        if r > 1.0:
            return None  # Miss

        # Bulls
        if r <= 0.05:
            return 50, 1
        if r <= 0.10:
            return 25, 1

        angle = math.degrees(math.atan2(y, x))
        angle = (angle + 90) % 360  # align 0° to top

        slice_index = int(angle // 18)
        base_score = DART_NUMBERS[slice_index]

        # Rings
        if 0.55 <= r <= 0.60:
            return base_score, 3
        elif 0.90 <= r <= 1.00:
            return base_score, 2
        else:
            return base_score, 1

    def board_to_screen(self, x, y, center, radius):
        sx = int(center[0] + x * radius)
        sy = int(center[1] - y * radius)  # y inverted for screen coords
        return sx, sy

    def draw(self):
        self.screen.fill((25, 25, 25))
        self.draw_header()
        self.draw_board()
        self.draw_info_panel()
        self.draw_footer()
        self.next_button.draw(self.screen)

    def draw_header(self):
        title = self.font_large.render("301 Game", True, (255, 255, 255))
        self.screen.blit(title, (20, 10))

    def draw_board(self):
        width, height = self.screen.get_size()

        self.board_center = (int(width * 0.4), height // 2)
        self.board_radius = int(min(width, height) * 0.4)

        cx, cy = self.board_center
        R = self.board_radius
        # Bullseyes
        pygame.draw.circle(self.screen, GREEN, self.board_center, int(R * 0.10))
        pygame.draw.circle(self.screen, RED, self.board_center, int(R * 0.05))

        for i in range(20):
            start = math.radians(-90 + i * 18)
            end = math.radians(-90 + (i + 1) * 18)

            base_color = SLICE_COLORS[i % 2]

            # Single inner
            self.draw_wedge(start, end, R * 0.10, R * 0.55, base_color)

            # Triple
            triple_color = RED if i % 2 == 0 else GREEN
            self.draw_wedge(start, end, R * 0.55, R * 0.60, triple_color)

            # Single outer
            self.draw_wedge(start, end, R * 0.60, R * 0.90, base_color)

            # Double
            double_color = RED if i % 2 == 0 else GREEN
            self.draw_wedge(start, end, R * 0.90, R * 1.00, double_color)

        # Numbers
        for i, number in enumerate(DART_NUMBERS):
            angle = math.radians(-90 + i * 18 + 9)
            tx = cx + math.cos(angle) * (R * 1.10)
            ty = cy + math.sin(angle) * (R * 1.10)
            label = self.font_small.render(str(number), True, (255, 255, 255))
            self.screen.blit(label, label.get_rect(center=(tx, ty)))

        # Impacts
        for x, y in self.impacts:
            sx, sy = self.board_to_screen(x, y, self.board_center, self.board_radius)
            pygame.draw.circle(self.screen, (255, 0, 0), (sx, sy), 6)

    def draw_info_panel(self):
        x = self.width - 300
        y = self.height * 0.05

        for i, player in enumerate(self.players):
            color = (255, 255, 0) if i == self.current_player else (255, 0, 0)
            label = self.font_large.render(
                f"Player {i+1}: {player['score']}", True, color
            )
            self.screen.blit(label, (x, y))
            y += 50

        y += 20
        turn = self.font_small.render(
            f"Current Turn: Player {self.current_player}", True, (255, 255, 255)
        )
        self.screen.blit(turn, (x, y))

        y += 40
        if self.last_throw:
            score, mult = self.last_throw
            text = f"Last Throw: {mult} × {score} = {score * mult}"
        else:
            text = "Last Throw: —"

        last = self.font_small.render(text, True, (180, 180, 180))
        self.screen.blit(last, (x, y))

    def draw_footer(self):
        status = self.font_small.render(
            "Status: Press SPACE to simulate throw", True, (160, 160, 160)
        )
        self.screen.blit(status, (20, 560))
