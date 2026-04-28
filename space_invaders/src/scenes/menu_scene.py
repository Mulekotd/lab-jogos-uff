
from pathlib import Path

from pplay.sprite import Sprite

from src.system.enums import Scenes


class MenuScene:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.mouse = game.window.get_mouse()
        self.images_dir = Path(self.game.settings.assets_dir) / "images"

        self.buttons = []
        self._build_buttons()

    def _build_buttons(self):
        actions = [
            ("button_play.png", Scenes.GAME_SCENE),
            ("button_dificuldade.png", Scenes.DIFFICULTY_SCENE),
            ("button_ranking.png", Scenes.RANKING_SCENE),
            ("button_sair.png", self.game.window.close),
        ]

        button_width = 200
        button_height = 50
        spacing = 18
        
        total_height = len(actions) * button_height + (len(actions) - 1) * spacing
        start_y = (self.game.settings.window_height - total_height) / 2

        for index, (image_name, action) in enumerate(actions):
            button = Sprite(str((self.images_dir / image_name).resolve()))
            button.x = (self.game.settings.window_width - button_width) / 2
            button.y = start_y + index * (button_height + spacing)

            self.buttons.append({"sprite": button, "action": action})

    def handle_input(self):
        if not self.mouse.is_button_pressed(self.mouse.BUTTON_LEFT):
            return

        for button in self.buttons:
            if self.mouse.is_over_object(button["sprite"]):
                if callable(button["action"]):
                    button["action"]()
                else:
                    self.game.change_scene(button["action"])
                break

    def update(self):
        pass

    def draw(self):
        self.window.set_background_color(self.game.settings.background_color)

        for button in self.buttons:
            button["sprite"].draw()

