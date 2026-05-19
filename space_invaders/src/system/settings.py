from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GameSettings:
    window_width: int = 480
    window_height: int = 720

    title: str = "Space Invaders"

    background_color: tuple[int, int, int] = (0, 0, 0)
    assets_dir: Path = Path(__file__).resolve().parents[1] / "assets"
    alien_rows: int = 6
    alien_cols: int = 6
