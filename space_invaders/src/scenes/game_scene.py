from src.system.enums import Scenes, Difficulties
from src.entities.player import Player


class GameScene:
	def __init__(self, game):
		self.game = game
		self.window = game.window
		self.keyboard = game.keyboard
		self.assets_dir = game.settings.assets_dir
		player_speed = 300
		player_fire_rate = self._get_fire_rate_from_difficulty()

		self.player = Player(
			self.window.width / 2 - 25,
			self.window.height - 60,
			player_speed,
			player_fire_rate,
			self.assets_dir
		)
		
		self.bullets = []

	def _get_fire_rate_from_difficulty(self):
		if self.game.current_difficulty == Difficulties.EASY:
			return 0.5
		elif self.game.current_difficulty == Difficulties.MEDIUM:
			return 0.3
		elif self.game.current_difficulty == Difficulties.HARD:
			return 0.15

		return 0.5

	def handle_input(self):
		if self.keyboard.key_pressed("ESC"):
			self.game.change_scene(Scenes.MENU_SCENE)
		
		if self.keyboard.key_pressed("space"):
			bullet = self.player.shoot()

			if bullet:
				self.bullets.append(bullet)

	def update(self, dt):
		self.player.update(dt, self.keyboard, self.window.width)
		
		for bullet in self.bullets[:]:
			bullet.update(dt)

			if not bullet.is_on_screen():
				self.bullets.remove(bullet)

	def draw(self):
		self.window.set_background_color((0, 0, 0))

		self.player.draw()

		for bullet in self.bullets:
			bullet.draw()
