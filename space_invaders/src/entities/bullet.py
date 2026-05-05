from pplay.sprite import Sprite


class Bullet:
    def __init__(self, x, y, speed, assets_dir):
        self.sprite = Sprite(str(assets_dir / "images" / "bullet.png"))
        self.sprite.set_position(x, y)
        self.speed = speed
        self.active = True

    def update(self, dt):
        self.sprite.y -= self.speed * dt
        
        if self.sprite.y < -self.sprite.height:
            self.active = False

    def draw(self):
        if self.active:
            self.sprite.draw()

    def is_on_screen(self):
        return self.active
