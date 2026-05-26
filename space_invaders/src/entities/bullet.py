from pplay.legacy.sprite import Sprite


class Bullet:
    def __init__(self, x, y, speed, bullet_asset, assets_dir, direction=-1, window_height=720):
        self.sprite = Sprite(str(assets_dir / "images" / bullet_asset))
        self.sprite.set_position(x, y)
        self.speed = speed
        self.direction = direction
        self.window_height = window_height
        self.active = True

    def update(self, dt):
        self.sprite.y += self.speed * dt * self.direction
        
        if self.direction < 0 and self.sprite.y < -self.sprite.height:
            self.active = False
        elif self.direction > 0 and self.sprite.y > self.window_height:
            self.active = False

    def draw(self):
        if self.active:
            self.sprite.draw()

    def is_on_screen(self):
        return self.active
