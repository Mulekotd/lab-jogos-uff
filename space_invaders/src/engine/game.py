from pplay.keyboard import Keyboard
from pplay.window import Window

from src.system.enums import Scenes
from src.system.settings import GameSettings
from src.scenes.difficulty_scene import DifficultyScene
from src.scenes.game_scene import GameScene
from src.scenes.menu_scene import MenuScene
from src.scenes.score_scene import ScoreScene


class SpaceInvaders:
    def __init__(self):
        self.is_running = 1

        self.settings = GameSettings()
        self.current_difficulty = None

        self.keyboard = Keyboard()
        self.window = Window(self.settings.window_width, self.settings.window_height)
        self.window.set_title(self.settings.title)

        self.scenes = {
            Scenes.MENU_SCENE: MenuScene(self),
            Scenes.GAME_SCENE: GameScene(self),
            Scenes.DIFFICULTY_SCENE: DifficultyScene(self),
            Scenes.RANKING_SCENE: ScoreScene(self),
        }

        self.current_scene = self.scenes[Scenes.MENU_SCENE]

    def change_scene(self, scene_id):
        self.current_scene = self.scenes[scene_id]

    def run(self):
        while self.is_running:
            self.dt = self.window.delta_time()
            self.current_scene.handle_input()
            self.current_scene.update()
            self.current_scene.draw()
            self.window.update()
