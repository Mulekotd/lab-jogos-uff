from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from pplay.legacy.gameimage import load_image
from pplay.legacy.window import Window


class Animation:
    def __init__(self, sprite_path: str | Path, width: int, height: int, gap: int, actions: Iterable[str], frame_rate: int = 120):
        self.sprite_path = Path(sprite_path)
        self.frame_width = max(1, int(width))
        self.frame_height = max(1, int(height))
        self.gap = max(0, int(gap))
        self.actions = list(actions)
        self.frame_rate = max(1, int(frame_rate))

        self.sheet, _ = load_image(str(self.sprite_path), alpha=True)
        self.frames: dict[str, list[Any]] = {action: [] for action in self.actions}
        self.current_action = self.actions[0] if self.actions else ""
        self.current_index = 0
        self.elapsed_ms = 0
        self.x = 0.0
        self.y = 0.0

        self._slice_frames()

    def _slice_frames(self):
        if not self.actions:
            return

        sheet_width = self.sheet.get_width()
        sheet_height = self.sheet.get_height()
        row_height = self.frame_height
        row_step = self.frame_height + self.gap

        for row_index, action in enumerate(self.actions):
            row_y = row_index * row_step
            if row_y >= sheet_height:
                break

            frames: list[Any] = []
            frame_x = self._find_first_opaque_column(row_y, min(sheet_height, row_y + row_height))

            if frame_x is None:
                self.frames[action] = []
                continue

            while frame_x + self.frame_width <= sheet_width:
                frame_rect = (frame_x, row_y, self.frame_width, row_height)
                frame = self.sheet.subsurface(frame_rect).copy()
                frames.append(frame)
                frame_x += self.frame_width + self.gap

            self.frames[action] = frames

    def _find_first_opaque_column(self, top: int, bottom: int) -> int | None:
        for x in range(self.sheet.get_width()):
            for y in range(top, bottom):
                if self.sheet.get_at((x, y)).a > 0:
                    return x
        return None

    def play(self, action: str):
        if action == self.current_action:
            return

        self.current_action = action
        self.current_index = 0
        self.elapsed_ms = 0

    def update(self, dt: float):
        frames = self.frames.get(self.current_action, [])

        if not frames:
            return

        self.elapsed_ms += int(dt * 1000)
        while self.elapsed_ms >= self.frame_rate:
            self.elapsed_ms -= self.frame_rate
            self.current_index = (self.current_index + 1) % len(frames)

    def get_frame(self):
        frames = self.frames.get(self.current_action, [])

        if not frames:
            return None

        return frames[self.current_index]

    def set_position(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    @property
    def width(self):
        frame = self.get_frame()
        return frame.get_width() if frame is not None else self.frame_width

    @property
    def height(self):
        frame = self.get_frame()
        return frame.get_height() if frame is not None else self.frame_height

    def draw(self):
        frame = self.get_frame()
        if frame is None:
            return

        window = Window.get_screen()

        if window is None:
            return

        window.blit(frame, (int(self.x), int(self.y)))
