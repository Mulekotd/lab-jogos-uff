from pplay.sprite import Sprite

from src.system.settings import GameSettings

from .paddle import Paddle


class Ball:
    def __init__(self, sprite: Sprite, settings: GameSettings):
        self.sprite = sprite
        self.settings = settings
        self.vx, self.vy = self._initial_velocity()

    @property
    def x(self):
        return self.sprite.x

    @x.setter
    def x(self, value):
        self.sprite.x = value

    @property
    def y(self):
        return self.sprite.y

    @y.setter
    def y(self, value):
        self.sprite.y = value

    @property
    def width(self):
        return self.sprite.width

    @property
    def height(self):
        return self.sprite.height

    def _initial_velocity(self):
        vx = self.settings.initial_ball_speed_x * 1.0
        vy = self.settings.initial_ball_speed_y * 1.0
        
        return vx, vy

    def reset_to_center(self, window_width: float, window_height: float):
        self.x = (window_width / 2) - (self.width / 2)
        self.y = (window_height / 2) - (self.height / 2)

        self.vx, self.vy = self._initial_velocity()

    def move(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def bounce_top_bottom(self, window_height: float):
        if self.y <= 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif (self.y + self.height) >= window_height:
            self.y = window_height - self.height
            self.vy = -abs(self.vy)

    def _speed_up(self, value: float):
        direction = -1 if value < 0 else 1
        new_speed = min(abs(value) * self.settings.speed_factor, self.settings.max_speed)

        return direction * new_speed

    def collide_with_paddle(self, paddle: Paddle, is_left_paddle: bool):
        if not self.sprite.collided(paddle.sprite):
            return

        if is_left_paddle and self.vx < 0:
            self.x = paddle.x + paddle.width
            self.vx = abs(self._speed_up(self.vx))
        elif (not is_left_paddle) and self.vx > 0:
            self.x = paddle.x - self.width
            self.vx = -abs(self._speed_up(self.vx))
        else:
            return

        hit_pos = ((self.y + self.height / 2) - (paddle.y + paddle.height / 2))
        normalized = hit_pos / (paddle.height / 2)

        self.vy += normalized * 180
        self.vy = max(-self.settings.max_speed, min(self.vy, self.settings.max_speed))

    def draw(self):
        self.sprite.draw()
