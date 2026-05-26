from random import randint, choice

from src.entities.alien_formation import AlienFormation
from src.entities.bullet import Bullet
from src.entities.player import Player
from src.system.enums import Scenes, Difficulties


class GameScene:
	def __init__(self, game):
		self.game = game
		self.window = game.window
		self.keyboard = game.keyboard

		self.assets_dir = game.settings.assets_dir
		self.player_spawn_x = self.window.width / 2 - 25
		self.player_spawn_y = self.window.height - 60

		self.fps_value = 0
		self.fps_elapsed = 0.0
		self.fps_frame_count = 0
		self.player_total_lives = self._get_player_lives_from_difficulty()
		self.player_current_lives = self.player_total_lives
		self.player_invincible_time = 0.0
		self.player_blink_elapsed = 0.0
		self.player_visible = True
		self.player_blink_interval = 0.15

		self.enemy_bullets = []
		self.enemy_fire_rate = self._get_enemy_fire_rate_from_difficulty()
		self.enemy_fire_timer = 0.0
		self.enemy_fire_cooldown = self._roll_enemy_fire_cooldown()

		player_speed = self._get_player_speed_from_difficulty()
		player_fire_rate = self._get_fire_rate_from_difficulty()

		self.player = Player(
			self.player_spawn_x,
			self.player_spawn_y,
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

	def _get_live_aliens(self):
		return [alien for row in self.aliens.matrix for alien in row]

	def _get_formation_bounds(self):
		live_aliens = self._get_live_aliens()
		if not live_aliens:
			return None

		left = min(alien.x for alien in live_aliens)
		right = max(alien.x + alien.width for alien in live_aliens)
		top = min(alien.y for alien in live_aliens)
		bottom = max(alien.y + alien.height for alien in live_aliens)

		return left, right, top, bottom

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

	def _get_player_lives_from_difficulty(self):
		if self.game.current_difficulty == Difficulties.EASY:
			return 8
		elif self.game.current_difficulty == Difficulties.MEDIUM:
			return 5
		elif self.game.current_difficulty == Difficulties.HARD:
			return 3
		return 5

	def _get_enemy_fire_rate_from_difficulty(self):
		if self.game.current_difficulty == Difficulties.EASY:
			return 1.2
		elif self.game.current_difficulty == Difficulties.MEDIUM:
			return 0.9
		elif self.game.current_difficulty == Difficulties.HARD:
			return 0.7
		return 0.9

	def _roll_enemy_fire_cooldown(self):
		scale = randint(85, 120) / 100.0
		return self.enemy_fire_rate * scale

	def _reset_player_position(self):
		self.player.set_position(self.player_spawn_x, self.player_spawn_y)

	def _take_player_damage(self):
		if self.player_invincible_time > 0:
			return

		self.player_current_lives -= 1
		self._reset_player_position()
		self.player_invincible_time = 2.0
		self.player_blink_elapsed = 0.0
		self.player_visible = False

		if self.player_current_lives <= 0:
			self.game.change_scene(Scenes.MENU_SCENE)

	def _fire_enemy_bullet(self):
		live_aliens = self._get_live_aliens()
		if not live_aliens:
			return

		alien = choice(live_aliens)
		bullet_x = alien.x + alien.width / 2
		bullet_y = alien.y + alien.height
		bullet = Bullet(
			bullet_x,
			bullet_y,
			speed=250,
			bullet_asset="alien_bullet.png",
			assets_dir=self.assets_dir,
			direction=1,
			window_height=self.window.height
		)
		self.enemy_bullets.append(bullet)

	def _update_enemy_fire(self, dt):
		if not self._has_alive_aliens():
			return

		self.enemy_fire_timer += dt
		if self.enemy_fire_timer >= self.enemy_fire_cooldown:
			self.enemy_fire_timer = 0.0
			self.enemy_fire_cooldown = self._roll_enemy_fire_cooldown()
			self._fire_enemy_bullet()

	def _update_player_invincibility(self, dt):
		if self.player_invincible_time <= 0:
			self.player_visible = True
			return

		self.player_invincible_time -= dt
		self.player_blink_elapsed += dt

		if self.player_blink_elapsed >= self.player_blink_interval:
			self.player_blink_elapsed = 0.0
			self.player_visible = not self.player_visible

		if self.player_invincible_time <= 0:
			self.player_invincible_time = 0.0
			self.player_visible = True

	def _check_player_hit(self, bullet):
		if self.player_invincible_time > 0:
			return False

		if bullet.sprite.collided(self.player.sprite):
			self._take_player_damage()
			return True

		return False

	def handle_input(self):
		if self.keyboard.key_pressed("ESC"):
			self.game.change_scene(Scenes.MENU_SCENE)
		
		if self.keyboard.key_pressed("SPACE"):
			bullet = self.player.shoot()

			if bullet:
				self.bullets.append(bullet)
	
	def check_collision(self, bullet, bounds=None):
		matrix = self.aliens.matrix
		if bounds is None:
			bounds = self._get_formation_bounds()

		if bounds is None:
			return False

		left, right, top, bottom = bounds

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
		self._update_player_invincibility(dt)

		if self.aliens.update(dt, self.window.width):
			self.game.change_scene(Scenes.MENU_SCENE)

		self._update_enemy_fire(dt)
		formation_bounds = self._get_formation_bounds()
		
		for bullet in self.bullets[:]:
			bullet.update(dt)
			hit = self.check_collision(bullet, formation_bounds)
		
			if hit:
				if bullet in self.bullets:
					self.bullets.remove(bullet)
				continue

			if not bullet.is_on_screen():
				if bullet in self.bullets:
					self.bullets.remove(bullet)

		for bullet in self.enemy_bullets[:]:
			bullet.update(dt)

			if self._check_player_hit(bullet):
				if bullet in self.enemy_bullets:
					self.enemy_bullets.remove(bullet)
				if self.player_current_lives <= 0:
					return
				continue

			if not bullet.is_on_screen():
				if bullet in self.enemy_bullets:
					self.enemy_bullets.remove(bullet)

		self._respawn_aliens_if_needed()

	def draw(self):
		self.window.set_background_color((0, 0, 0))

		self.aliens.draw()
		self.player.draw(self.player_visible)

		for bullet in self.bullets:
			bullet.draw()

		for bullet in self.enemy_bullets:
			bullet.draw()

		life_text = f"{self.player_current_lives}/{self.player_total_lives}"
		self.window.draw_text(life_text, 12, 12, 18, (220, 40, 40), "Arial", True)

		fps_text = f"FPS: {self.fps_value}"
		x = self.window.width - 12 - 96
		y = 12

		self.window.draw_text(fps_text, x, y, 14, (255, 255, 255), "Arial", True)
