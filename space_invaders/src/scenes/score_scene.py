from src.system.enums import Scenes
from src.system.ranking import load_top_ranking


class ScoreScene:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.keyboard = game.keyboard
        self.entries = []
    
    def reset_input_state(self):
        self.entries = load_top_ranking(5)

    def handle_input(self):
        if self.keyboard.key_pressed("ESC"):
            self.game.change_scene(Scenes.MENU_SCENE)

    def update(self, dt):
        pass

    def draw(self):
        self.window.set_background_color(self.game.settings.background_color)
        self._draw_centered_text("Ranking", 80, 40, (255, 255, 255), True)

        if not self.entries:
            self._draw_centered_text("Nenhum ranking salvo", 250, 22, (200, 200, 200), False)
            return

        header_y = 170
        self.window.draw_text("NAME", 60, header_y, 18, (180, 180, 180), "Arial", True)
        self.window.draw_text("SCORE", 180, header_y, 18, (180, 180, 180), "Arial", True)
        self.window.draw_text("DATE", 320, header_y, 18, (180, 180, 180), "Arial", True)

        for index, entry in enumerate(self.entries, start=1):
            y = header_y + 42 * index
            self.window.draw_text(f"{index}. {entry.name}", 60, y, 20, (255, 255, 255), "Arial", True)
            self.window.draw_text(str(entry.score), 180, y, 20, (255, 255, 255), "Arial", True)
            self.window.draw_text(entry.date, 320, y, 20, (255, 255, 255), "Arial", True)

    def _draw_centered_text(self, text, y, size, color, bold=False):
        text_width = len(text) * size * 0.58
        x = int((self.window.width - text_width) / 2)
        self.window.draw_text(text, x, y, size, color, "Arial", bold)
