from pplay.sprite import Sprite


class Paddle:
    def __init__(self, sprite: Sprite, speed: float):
        self.sprite = sprite
        self.speed = speed

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

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y

    def move_up(self, dt: float):
        self.y -= self.speed * dt

    def move_down(self, dt: float):
        self.y += self.speed * dt

    def clamp_to_window(self, window_height: float):
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > window_height:
            self.y = window_height - self.height

    def draw(self):
        self.sprite.draw()

