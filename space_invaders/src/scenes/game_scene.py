from random import randint, choice

from src.entities.alien_formation import AlienFormation
from src.entities.bullet import Bullet
from src.entities.player import Player
from src.system.enums import Scenes, Difficulties
from src.system.ranking import save_ranking_entry


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
		self.score = 0
		self.current_wave = 1
		self.game_over = False
		self.game_over_screen_drawn = False
		self.ranking_saved = False
		self.player_total_lives = self._get_player_lives_from_difficulty()
		self.player_current_lives = self.player_total_lives
		self.player_invincible_time = 0.0
		self.player_blink_elapsed = 0.0
		self.player_visible = True
		self.player_blink_interval = 0.15

		self.enemy_bullets = []
		self.base_enemy_fire_rate = self._get_enemy_fire_rate_from_difficulty()
		self.enemy_fire_rate = self._get_enemy_fire_rate_for_wave()
		self.enemy_fire_timer = 0.0
		self.enemy_fire_cooldown = self._roll_enemy_fire_cooldown()

		player_speed = self._get_player_speed_from_difficulty()
		player_fire_rate = self._get_fire_rate_from_difficulty()

		self.player = Player(
			assets_dir=self.assets_dir,
			x=self.player_spawn_x,
			y=self.player_spawn_y,
			speed=player_speed,
			fire_rate=player_fire_rate
		)
		
		self.bullets = []
		self.aliens = self._create_aliens()

	def reset_input_state(self):
		pass

	def _create_aliens(self):
		rows, cols = self._get_formation_size_for_wave()
		return AlienFormation(
			rows=rows,
			cols=cols,
			assets_dir=self.assets_dir,
			window_width=self.window.width,
			player_y=self.player.sprite.y,
			speed=self._get_alien_speed_for_wave()
		)

	def _has_alive_aliens(self):
		return any(line for line in self.aliens.matrix)

	def _respawn_aliens_if_needed(self):
		if not self._has_alive_aliens():
			self.current_wave += 1
			self.bullets.clear()
			self.enemy_bullets.clear()
			self.enemy_fire_timer = 0.0
			self.enemy_fire_rate = self._get_enemy_fire_rate_for_wave()
			self.enemy_fire_cooldown = self._roll_enemy_fire_cooldown()
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

	def _get_wave_multiplier(self):
		return 1.0 + (self.current_wave - 1) * 0.08

	def _get_score_multiplier(self):
		return 1.0 + (self.current_wave - 1) * 0.12

	def _get_enemy_fire_rate_for_wave(self):
		return max(0.25, self.base_enemy_fire_rate / self._get_wave_multiplier())

	def _get_alien_speed_for_wave(self):
		return 55.0 * self._get_wave_multiplier()

	def _get_formation_size_for_wave(self):
		growth_steps = (self.current_wave - 1) // 5
		rows = min(6, 4 + growth_steps)
		cols = min(10, 4 + growth_steps * 2)
		return rows, cols

	def _get_alien_score(self, row_index):
		base_points = (self.aliens.rows - row_index) * 100
		return int(round(base_points * self._get_score_multiplier()))

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
			self._start_game_over()

	def _start_game_over(self):
		self.game_over = True
		self.game_over_screen_drawn = False

	def _save_score_and_return_to_menu(self):
		if self.ranking_saved:
			return

		print("\nGAME OVER")
		print(f"Pontuacao final: {self.score}")
		try:
			player_name = input("Digite seu nome para salvar no ranking: ")
		except EOFError:
			player_name = "ANONIMO"

		save_ranking_entry(player_name, self.score)
		self.ranking_saved = True
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
		if self.game_over:
			return

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

		for row_index in range(len(matrix) - 1, -1, -1):
			line = matrix[row_index]
			for alien in list(line):
				if bullet.sprite.collided(alien):
					line.remove(alien)
					return self._get_alien_score(row_index)

		return 0

	def update(self, dt):
		if self.game_over:
			if self.game_over_screen_drawn and not self.ranking_saved:
				self._save_score_and_return_to_menu()
			return

		self.fps_elapsed += dt
		self.fps_frame_count += 1

		if self.fps_elapsed >= 1.0:
			self.fps_value = int(round(self.fps_frame_count / self.fps_elapsed))
			self.fps_elapsed = 0.0
			self.fps_frame_count = 0

		self.player.update(dt, self.keyboard, self.window.width)
		self._update_player_invincibility(dt)

		if self.aliens.update(dt, self.window.width):
			self._start_game_over()
			return

		self._update_enemy_fire(dt)
		formation_bounds = self._get_formation_bounds()
		
		for bullet in self.bullets[:]:
			bullet.update(dt)
			hit_score = self.check_collision(bullet, formation_bounds)
		
			if hit_score:
				self.score += hit_score
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

		if self.game_over:
			self._draw_game_over()
			self.game_over_screen_drawn = True
			return

		self.aliens.draw()
		self.player.draw(self.player_visible)

		for bullet in self.bullets:
			bullet.draw()

		for bullet in self.enemy_bullets:
			bullet.draw()

		life_text = f"{self.player_current_lives}/{self.player_total_lives}"
		self.window.draw_text(life_text, 12, 12, 18, (220, 40, 40), "Arial", True)

		wave_text = f"WAVE: {self.current_wave}"
		self.window.draw_text(wave_text, 12, 36, 14, (180, 180, 180), "Arial", True)

		score_text = f"SCORE: {self.score}"
		self._draw_centered_text(score_text, 12, 20, (255, 255, 255), True)

		fps_text = f"FPS: {self.fps_value}"
		x = self.window.width - 12 - 64
		y = 12

		self.window.draw_text(fps_text, x, y, 14, (255, 255, 255), "Arial", True)

	def _draw_game_over(self):
		self._draw_centered_text("GAME OVER", 260, 42, (255, 70, 70), True)
		self._draw_centered_text(f"SCORE: {self.score}", 320, 24, (255, 255, 255), True)

	def _draw_centered_text(self, text, y, size, color, bold=False):
		text_width = len(text) * size * 0.58
		x = int((self.window.width - text_width) / 2)
		self.window.draw_text(text, x, y, size, color, "Arial", bold)
