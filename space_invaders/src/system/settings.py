from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GameSettings:
    window_width: int = 800
    window_height: int = 580

    title: str = "Space Invaders"

    background_color: tuple[int, int, int] = (0, 0, 0)
    assets_dir: Path = Path(__file__).resolve().parents[1] / "assets"
