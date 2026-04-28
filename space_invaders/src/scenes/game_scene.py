from src.system.enums import Scenes


class GameScene:
	def __init__(self, game):
		self.game = game
		self.window = game.window
		self.keyboard = game.keyboard

	def handle_input(self):
		if self.keyboard.key_pressed("ESC"):
			self.game.change_scene(Scenes.MENU_SCENE)

	def update(self):
		pass

	def draw(self):
		self.window.set_background_color((0, 0, 0))
