from dataclasses import dataclass


@dataclass(frozen=True)
class GameSettings:
    window_width: int = 800
    window_height: int = 580

    title: str = "Pong"

    max_speed: float = 1200.0
    speed_factor: float = 1.08

    paddle_speed: float = 500.0
    
    ai_speed: float = 460.0
    ai_dead_zone: float = 12.0

    initial_ball_speed_x: float = 420.0
    initial_ball_speed_y: float = 240.0

    background_color: tuple[int, int, int] = (18, 150, 36)
