from src.entities.alien_formation import AlienFormation
from src.entities.player import Player
from src.system.enums import Scenes, Difficulties


class GameScene:
	def __init__(self, game):
		self.game = game
		self.window = game.window
		self.keyboard = game.keyboard
		self.assets_dir = game.settings.assets_dir
		player_speed = self._get_player_speed_from_difficulty()
		player_fire_rate = self._get_fire_rate_from_difficulty()

		self.player = Player(
			self.window.width / 2 - 25,
			self.window.height - 60,
			player_speed,
			player_fire_rate,
			self.assets_dir
		)
		
		self.bullets = []
		self.aliens = AlienFormation(
			self.game.settings.alien_rows,
			self.game.settings.alien_cols,
			self.assets_dir,
			self.window.width,
			self.player.sprite.y
		)

	def reset_input_state(self):
		pass

	def _get_player_speed_from_difficulty(self):
		if self.game.current_difficulty == Difficulties.EASY:
			return 400
		elif self.game.current_difficulty == Difficulties.MEDIUM:
			return 300
		elif self.game.current_difficulty == Difficulties.HARD:
			return 200
		return 300

	def _get_fire_rate_from_difficulty(self):
		if self.game.current_difficulty == Difficulties.EASY:
			return 0.3
		elif self.game.current_difficulty == Difficulties.MEDIUM:
			return 0.5
		elif self.game.current_difficulty == Difficulties.HARD:
			return 0.8
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

		if self.aliens.update(dt, self.window.width):
			self.game.change_scene(Scenes.MENU_SCENE)
		
		for bullet in self.bullets[:]:
			bullet.update(dt)

			if not bullet.is_on_screen():
				self.bullets.remove(bullet)

	def draw(self):
		self.window.set_background_color((0, 0, 0))

		self.aliens.draw()
		self.player.draw()

		for bullet in self.bullets:
			bullet.draw()

		fps = 0 if self.game.dt <= 0 else int(round(1.0 / self.game.dt))
		fps_text = f"FPS: {fps}"

		x = self.window.width - 80
		y = 12

		self.window.draw_text(fps_text, x, y, 14, (255, 255, 255), "Arial", True)
