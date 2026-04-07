from pathlib import Path

from pplay.keyboard import Keyboard
from pplay.sprite import Sprite
from pplay.window import Window

from src.entities.ball import Ball
from src.entities.paddle import Paddle

from src.system.settings import GameSettings


class PongGame:
    def __init__(self):
        self.settings = GameSettings()

        self.window = Window(self.settings.window_width, self.settings.window_height)
        self.window.set_title(self.settings.title)

        self.keyboard = Keyboard()

        self._load_entities()

        self.is_running = True
        self.waiting_start = True

        self.player_score = 0
        self.enemy_score = 0

    def _load_entities(self):
        base_dir = Path(__file__).resolve().parent.parent
        images_dir = base_dir / "assets" / "images"

        ball_sprite   = Sprite(str(images_dir / "ball.png"))
        player_sprite = Sprite(str(images_dir / "player.png"))
        enemy_sprite  = Sprite(str(images_dir / "enemy.png"))

        self.ball   = Ball(ball_sprite, self.settings)
        self.player = Paddle(player_sprite, self.settings.paddle_speed)
        self.enemy  = Paddle(enemy_sprite, self.settings.ai_speed)

        self.ball.reset_to_center(self.window.width, self.window.height)

        self.player.x = self.player.width
        self.player.y = (self.window.height / 2) - (self.player.height / 2)

        self.enemy.x = self.window.width - 2 * self.enemy.width
        self.enemy.y = (self.window.height / 2) - (self.enemy.height / 2)

    def _handle_input(self, dt: float):
        if self.keyboard.key_pressed("ESC"):
            self.is_running = False
            self.window.close()

        if self.waiting_start:
            if self.keyboard.key_pressed("SPACE"):
                self.waiting_start = False
            return

        if self.keyboard.key_pressed("UP"):
            self.player.move_up(dt)

        if self.keyboard.key_pressed("DOWN"):
            self.player.move_down(dt)

    def _update_enemy_ai(self, dt: float):
        if self.ball.vx > 0:
            target_y = self.ball.y + (self.ball.height / 2)
        else:
            target_y = self.window.height / 2

        enemy_center = self.enemy.y + (self.enemy.height / 2)

        diff = target_y - enemy_center

        if abs(diff) <= self.settings.ai_dead_zone:
            return

        if diff > 0:
            self.enemy.move_down(dt)
        else:
            self.enemy.move_up(dt)

    def _update_ball(self):
        if self.waiting_start:
            return

        self.ball.move(self.dt)
        self.ball.bounce_top_bottom(self.window.height)
        self.ball.collide_with_paddle(self.player, is_left_paddle=True)
        self.ball.collide_with_paddle(self.enemy, is_left_paddle=False)

        if (self.ball.x + self.ball.width) < 0:
            self.enemy_score += 1

            self.ball.reset_to_center(self.window.width, self.window.height)
            self.player.set_position(self.player.width, (self.window.height / 2) - (self.player.height / 2))
            self.enemy.set_position(self.window.width - 2 * self.enemy.width, (self.window.height / 2) - (self.enemy.height / 2))

            self.waiting_start = True
        elif self.ball.x > self.window.width:
            self.player_score += 1

            self.ball.reset_to_center(self.window.width, self.window.height)
            self.player.set_position(self.player.width, (self.window.height / 2) - (self.player.height / 2))
            self.enemy.set_position(self.window.width - 2 * self.enemy.width, (self.window.height / 2) - (self.enemy.height / 2))

            self.waiting_start = True

    def _clamp_paddles(self):
        self.player.clamp_to_window(self.window.height)
        self.enemy.clamp_to_window(self.window.height)

    def _draw_hud(self):
        score_text = f"{self.player_score}   X   {self.enemy_score}"

        self.window.draw_text(
            score_text,
            (self.window.width / 2) - 45,
            20,
            size=34,
            color=(255, 255, 255),
            bold=True,
        )

    def _render(self):
        self.window.set_background_color(self.settings.background_color)
        
        self.player.draw()
        self.enemy.draw()
        self.ball.draw()
        self._draw_hud()

        self.window.update()

    def run(self):
        while self.is_running:
            self.dt = self.window.delta_time()
            self._handle_input(self.dt)
            self._update_enemy_ai(self.dt)
            self._update_ball()
            self._clamp_paddles()
            self._render()
