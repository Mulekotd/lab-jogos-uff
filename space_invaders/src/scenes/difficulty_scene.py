
from pathlib import Path

from pplay.sprite import Sprite

from src.system.enums import Difficulties, Scenes


class DifficultyScene:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.mouse = game.window.get_mouse()
        self.images_dir = Path(self.game.settings.assets_dir) / "images"

        self.buttons = []
        self._build_buttons()

    def _build_buttons(self):
        options = [
            ("button_facil.png", Difficulties.EASY),
            ("button_medio.png", Difficulties.MEDIUM),
            ("button_dificil.png", Difficulties.HARD),
        ]

        button_width = 200
        button_height = 50
        spacing = 18

        total_height = len(options) * button_height + (len(options) - 1) * spacing
        start_y = (self.game.settings.window_height - total_height) / 2

        for index, (image_name, difficulty) in enumerate(options):
            button = Sprite(str((self.images_dir / image_name).resolve()))
            button.x = (self.game.settings.window_width - button_width) / 2
            button.y = start_y + index * (button_height + spacing)

            self.buttons.append({"sprite": button, "difficulty": difficulty})

    def handle_input(self):
        if self.mouse.is_button_pressed(self.mouse.BUTTON_LEFT):
            for button in self.buttons:
                if self.mouse.is_over_object(button["sprite"]):
                    self.game.current_difficulty = button["difficulty"]
                    break

        if self.game.keyboard.key_pressed("ESC"):
            self.game.change_scene(Scenes.MENU_SCENE)

    def update(self):
        pass

    def draw(self):
        self.window.set_background_color(self.game.settings.background_color)

        for button in self.buttons:
            button["sprite"].draw()