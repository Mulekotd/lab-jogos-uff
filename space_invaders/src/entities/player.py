

from pplay.sprite import Sprite
from .bullet import Bullet


class Player:
    def __init__(self, x, y, speed, fire_rate, assets_dir):
        self.sprite = Sprite(str(assets_dir / "images" / "player.png"))
        self.sprite.set_position(x, y)
        self.speed = speed
        self.fire_rate = fire_rate
        self.assets_dir = assets_dir
        self.fire_cooldown = 0.0

    def update(self, dt, keyboard, window_width):
        if keyboard.key_pressed("left"):
            self.sprite.x -= self.speed * dt

        if keyboard.key_pressed("right"):
            self.sprite.x += self.speed * dt

        if self.sprite.x < -self.sprite.width:
            self.sprite.x = window_width
        elif self.sprite.x > window_width:
            self.sprite.x = -self.sprite.width

        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt

    def shoot(self):
        if self.fire_cooldown <= 0:
            self.fire_cooldown = self.fire_rate
            bullet = Bullet(self.sprite.x + self.sprite.width / 2, self.sprite.y, 400, self.assets_dir)

            return bullet

        return None

    def draw(self):
        self.sprite.draw()
