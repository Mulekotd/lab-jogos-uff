from src.entities.alien_formation import AlienFormation
from src.entities.player import Player
from src.system.enums import Scenes, Difficulties


class GameScene:
	def __init__(self, game):
		self.game = game
		self.window = game.window
		self.keyboard = game.keyboard
		self.assets_dir = game.settings.assets_dir
		self.fps_value = 0
		self.fps_elapsed = 0.0
		self.fps_frame_count = 0
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
		self.aliens = self._create_aliens()

	def reset_input_state(self):
		pass

	def _create_aliens(self):
		return AlienFormation(
			self.game.settings.alien_rows,
			self.game.settings.alien_cols,
			self.assets_dir,
			self.window.width,
			self.player.sprite.y
		)

	def _has_alive_aliens(self):
		return any(line for line in self.aliens.matrix)

	def _respawn_aliens_if_needed(self):
		if not self._has_alive_aliens():
			self.aliens = self._create_aliens()

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
		
		if self.keyboard.key_pressed("SPACE"):
			bullet = self.player.shoot()

			if bullet:
				self.bullets.append(bullet)
	
	def check_collision(self, bullet):
		matrix = self.aliens.matrix
		if not any(matrix):
			return False

		live_aliens = [alien for row in matrix for alien in row]
		if not live_aliens:
			return False

		left = min(alien.x for alien in live_aliens)
		right = max(alien.x + alien.width for alien in live_aliens)
		top = min(alien.y for alien in live_aliens)
		bottom = max(alien.y + alien.height for alien in live_aliens)

		bx = bullet.sprite.x
		by = bullet.sprite.y

		bw = getattr(bullet.sprite, 'width', 0)
		bh = getattr(bullet.sprite, 'height', 0)

		if bx + bw < left or bx > right or by + bh < top or by > bottom:
			return False

		for line in reversed(matrix):
			for alien in list(line):
				if bullet.sprite.collided(alien):
					line.remove(alien)
					return True

		return False

	def update(self, dt):
		self.fps_elapsed += dt
		self.fps_frame_count += 1

		if self.fps_elapsed >= 1.0:
			self.fps_value = int(round(self.fps_frame_count / self.fps_elapsed))
			self.fps_elapsed = 0.0
			self.fps_frame_count = 0

		self.player.update(dt, self.keyboard, self.window.width)

		if self.aliens.update(dt, self.window.width):
			self.game.change_scene(Scenes.MENU_SCENE)
		
		for bullet in self.bullets[:]:
			bullet.update(dt)
			hit = self.check_collision(bullet)
		
			if hit:
				if bullet in self.bullets:
					self.bullets.remove(bullet)
				continue

			if not bullet.is_on_screen():
				if bullet in self.bullets:
					self.bullets.remove(bullet)

		self._respawn_aliens_if_needed()

	def draw(self):
		self.window.set_background_color((0, 0, 0))

		self.aliens.draw()
		self.player.draw()

		for bullet in self.bullets:
			bullet.draw()

		fps_text = f"FPS: {self.fps_value}"
		x = self.window.width - 12 - 96
		y = 12

		self.window.draw_text(fps_text, x, y, 14, (255, 255, 255), "Arial", True)
