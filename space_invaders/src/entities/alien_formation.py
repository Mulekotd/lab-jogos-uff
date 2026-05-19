from __future__ import annotations

from pathlib import Path

from pplay.legacy.sprite import Sprite


class AlienFormation:
    def __init__(self, rows: int, cols: int, assets_dir: Path, window_width: int, player_y: float):
        self.rows = max(4, int(rows))
        self.cols = max(6, int(cols))
        self.assets_dir = Path(assets_dir)
        self.window_width = window_width
        self.player_y = player_y

        self.direction = 1
        self.speed = 55.0
        self.drop_distance = 16
        self.drawn_once = False
        self.cell_width = 32
        self.cell_height = 32
        self.spacing_x = self.cell_width // 2
        self.spacing_y = self.cell_height // 2
        self.margin_top = 64

        self.matrix: list[list[Sprite]] = []
        self._build_matrix()

    def _build_matrix(self):
        total_width = self.cols * self.cell_width + (self.cols - 1) * self.spacing_x
        start_x = max(12, int((self.window_width - total_width) / 2))

        for row in range(self.rows):
            row_sprites: list[Sprite] = []
            for col in range(self.cols):
                alien_name = f"alien_{row % 6:02d}.png"
                sprite = Sprite(str(self.assets_dir / "images" / alien_name))
                sprite.set_position(
                    start_x + col * (self.cell_width + self.spacing_x),
                    self.margin_top + row * (self.cell_height + self.spacing_y),
                )
                row_sprites.append(sprite)
            self.matrix.append(row_sprites)

    def draw(self):
        for row in self.matrix:
            for alien in row:
                alien.draw()

        self.drawn_once = True

    def update(self, dt: float, window_width: int) -> bool:
        if not self.drawn_once:
            return False

        step = self.speed * dt
        if step <= 0:
            return False

        left_edge, right_edge = self._get_horizontal_bounds()
        if left_edge is None or right_edge is None:
            return False

        hit_left_wall = self.direction < 0 and left_edge - step <= 0
        hit_right_wall = self.direction > 0 and right_edge + step >= window_width

        if hit_left_wall or hit_right_wall:
            self.direction *= -1
            self._move_vertical(self.drop_distance)
        else:
            self._move_horizontal(self.direction * step)

        return self._reached_player_height()

    def _move_horizontal(self, delta_x: float):
        for row in self.matrix:
            for alien in row:
                alien.x += delta_x
                alien.set_position(alien.x, alien.y)

    def _move_vertical(self, delta_y: float):
        for row in self.matrix:
            for alien in row:
                alien.y += delta_y
                alien.set_position(alien.x, alien.y)

    def _get_horizontal_bounds(self):
        live_aliens = [alien for row in self.matrix for alien in row]

        if not live_aliens:
            return None, None

        left_edge = min(alien.x for alien in live_aliens)
        right_edge = max(alien.x + alien.width for alien in live_aliens)

        return left_edge, right_edge

    def _reached_player_height(self) -> bool:
        live_aliens = [alien for row in self.matrix for alien in row]

        if not live_aliens:
            return False

        lowest = max(alien.y + alien.height for alien in live_aliens)

        return lowest >= self.player_y
