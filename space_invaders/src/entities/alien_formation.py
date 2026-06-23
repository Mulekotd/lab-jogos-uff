from __future__ import annotations
import random

from pathlib import Path

from pplay.legacy.sprite import Sprite


class AlienFormation:
    def __init__(self, rows: int, cols: int, assets_dir: Path, window_width: int, player_y: float, speed: float = 55.0):
        self.rows = max(1, min(6, int(rows)))
        self.cols = max(1, min(10, int(cols)))
        self.assets_dir = Path(assets_dir)
        self.window_width = window_width
        self.player_y = player_y

        self.direction = 1
        self.speed = float(speed)
        self.drop_distance = 16
        self.drawn_once = False

        self.cell_width = 32
        self.cell_height = 32

        self.spacing_x = self.cell_width // 2
        self.spacing_y = self.cell_height // 2
        self.margin_top = 64

        self.matrix: list[list[Sprite]] = []
        self.alien_positions: dict[int, tuple[int, int]] = {}
        self.boss_position: tuple[int, int] | None = None
        self._build_matrix()

    def _build_matrix(self):
        total_width = self.cols * self.cell_width + (self.cols - 1) * self.spacing_x
        start_x = max(12, int((self.window_width - total_width) / 2))
        boss_position = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))

        self.matrix = []
        self.alien_positions = {}
        self.boss_position = boss_position

        for row in range(self.rows):
            row_sprites: list[Sprite] = []
            for col in range(self.cols):
                is_boss = (row, col) == boss_position
                alien_name = "alien_05.png" if is_boss else f"alien_{row % 5:02d}.png"
                sprite = self._create_sprite(
                    alien_name,
                    start_x + col * (self.cell_width + self.spacing_x),
                    self.margin_top + row * (self.cell_height + self.spacing_y)
                )

                row_sprites.append(sprite)
                self.alien_positions[id(sprite)] = (row, col)
            self.matrix.append(row_sprites)

    def _create_sprite(self, alien_name: str, x: float, y: float) -> Sprite:
        sprite = Sprite(str(self.assets_dir / "images" / alien_name))
        sprite.set_position(x, y)
        return sprite

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

    def get_live_aliens(self) -> list[Sprite]:
        return [alien for row in self.matrix for alien in row]

    def get_bounds(self):
        live_aliens = self.get_live_aliens()
        if not live_aliens:
            return None

        left_edge = min(alien.x for alien in live_aliens)
        right_edge = max(alien.x + alien.width for alien in live_aliens)
        top_edge = min(alien.y for alien in live_aliens)
        bottom_edge = max(alien.y + alien.height for alien in live_aliens)

        return left_edge, right_edge, top_edge, bottom_edge

    def check_bullet_collision(self, bullet_sprite: Sprite, bounds=None) -> list[tuple[int, int]]:
        if bounds is None:
            bounds = self.get_bounds()

        if bounds is None:
            return []

        left, right, top, bottom = bounds

        bx = bullet_sprite.x
        by = bullet_sprite.y
        bw = getattr(bullet_sprite, "width", 0)
        bh = getattr(bullet_sprite, "height", 0)

        if bx + bw < left or bx > right or by + bh < top or by > bottom:
            return []

        for row_index in range(len(self.matrix) - 1, -1, -1):
            line = self.matrix[row_index]
            for alien in list(line):
                if bullet_sprite.collided(alien):
                    return self._handle_alien_hit(alien)

        return []

    def _handle_alien_hit(self, alien: Sprite) -> list[tuple[int, int]]:
        alien_position = self.alien_positions.get(id(alien))
        if alien_position is None:
            return []

        if alien_position == self.boss_position:
            removed_positions = self._remove_aliens(self._get_adjacent_aliens(*alien_position))
            self._promote_new_boss()
            return removed_positions

        return self._remove_aliens([alien])

    def _get_adjacent_aliens(self, row_index: int, col_index: int) -> list[Sprite]:
        adjacent_aliens: list[Sprite] = []
        adjacent_positions = {
            (row_index, col_index),
            (row_index - 1, col_index),
            (row_index + 1, col_index),
            (row_index, col_index - 1),
            (row_index, col_index + 1)
        }

        for alien in self.get_live_aliens():
            alien_position = self.alien_positions.get(id(alien))
            if alien_position is None:
                continue

            if alien_position in adjacent_positions:
                adjacent_aliens.append(alien)

        return adjacent_aliens

    def _remove_aliens(self, aliens: list[Sprite]) -> list[tuple[int, int]]:
        removed_positions: list[tuple[int, int]] = []
        removed_ids: set[int] = set()

        for alien in aliens:
            alien_id = id(alien)
            if alien_id in removed_ids:
                continue

            position = self.alien_positions.get(alien_id)
            if position is None:
                continue

            if self._remove_alien_from_matrix(alien):
                self.alien_positions.pop(alien_id, None)

                removed_ids.add(alien_id)
                removed_positions.append(position)

        return removed_positions

    def _remove_alien_from_matrix(self, alien: Sprite) -> bool:
        for line in self.matrix:
            for index, current_alien in enumerate(line):
                if current_alien is alien:
                    del line[index]
                    return True

        return False

    def _promote_new_boss(self):
        live_aliens = self.get_live_aliens()
        if not live_aliens:
            self.boss_position = None
            return

        promoted_alien = random.choice(live_aliens)
        promoted_position = self.alien_positions.get(id(promoted_alien))

        if promoted_position is None:
            self.boss_position = None
            return

        if self._replace_alien_sprite(promoted_alien, "alien_05.png") is None:
            self.boss_position = None
            return

        self.boss_position = promoted_position

    def _replace_alien_sprite(self, alien: Sprite, alien_name: str) -> Sprite | None:
        alien_position = self.alien_positions.get(id(alien))
        if alien_position is None:
            return None

        replacement = self._create_sprite(alien_name, alien.x, alien.y)

        for line in self.matrix:
            for index, current_alien in enumerate(line):
                if current_alien is alien:
                    line[index] = replacement
                    self.alien_positions.pop(id(alien), None)
                    self.alien_positions[id(replacement)] = alien_position
                    return replacement

        return None

    def _get_horizontal_bounds(self):
        live_aliens = self.get_live_aliens()
        if not live_aliens:
            return None, None

        left_edge = min(alien.x for alien in live_aliens)
        right_edge = max(alien.x + alien.width for alien in live_aliens)
        return left_edge, right_edge

    def _reached_player_height(self) -> bool:
        live_aliens = self.get_live_aliens()
        if not live_aliens:
            return False

        lowest = max(alien.y + alien.height for alien in live_aliens)
        return lowest >= self.player_y
