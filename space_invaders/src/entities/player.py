
from pathlib import Path

from src.engine.animation import Animation
from .bullet import Bullet


class Player:
    def __init__(self, x, y, speed, fire_rate, assets_dir):
        self.animation = Animation(
            Path(assets_dir) / "images" / "player_spritesheet.png",
            width=34,
            height=38,
            gap=1,
            actions=["IDLE"],
            frame_rate=120
        )

        self.animation.play("IDLE")
        self.animation.set_position(x, y)

        self.speed = speed
        self.fire_rate = fire_rate
        self.assets_dir = assets_dir
        self.fire_cooldown = 0.0

    def update(self, dt, keyboard, window_width):
        self.animation.update(dt)

        if keyboard.key_pressed("LEFT") or keyboard.key_pressed("A"):
            self.animation.x -= self.speed * dt

        if keyboard.key_pressed("RIGHT") or keyboard.key_pressed("D"):
            self.animation.x += self.speed * dt

        if self.animation.x < -self.animation.width:
            self.animation.x = window_width
        elif self.animation.x > window_width:
            self.animation.x = -self.animation.width

        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt

    def shoot(self):
        if self.fire_cooldown <= 0:
            self.fire_cooldown = self.fire_rate
            bullet = Bullet(self.animation.x + self.animation.width / 2, self.animation.y, 400, self.assets_dir)

            return bullet

        return None

    def draw(self):
        self.animation.draw()

    @property
    def sprite(self):
        return self.animation
