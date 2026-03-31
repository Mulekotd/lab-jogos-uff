from pathlib import Path

from pplay.window import Window
from pplay.keyboard import Keyboard
from pplay.sprite import Sprite

base_dir = Path(__file__).resolve().parent


def move_ball(ball, vx, vy):
    ball.x += vx
    ball.y += vy


def speed_up(value, factor, max_speed):
    direction = -1 if value < 0 else 1
    new_speed = min(abs(value) * factor, max_speed)
    return direction * new_speed


def change_directions(window, ball, vx, vy):
    if ball.x <= 0:
        ball.x = 0
        vx *= -1
        vx = speed_up(vx, 1.12, 6)
        vy = speed_up(vy, 1.12, 6)
    elif (ball.x + ball.width) >= window.width:
        ball.x = window.width - ball.width
        vx *= -1
        vx = speed_up(vx, 1.12, 6)
        vy = speed_up(vy, 1.12, 6)

    if ball.y <= 0:
        ball.y = 0
        vy *= -1
    elif (ball.y + ball.height) >= window.height:
        ball.y = window.height - ball.height
        vy *= -1

    return vx, vy


def main():
    # Variáveis
    is_running = True
    
    # Objetos
    window = Window(800, 580)
    window.set_title("Pong")

    keyboard = Keyboard()

    ball = Sprite(str(base_dir / "src" / "assets" / "images" / "ball.png"))
    ball.x = (window.width / 2) - (ball.width / 2)
    ball.y = (window.height / 2) - (ball.height / 2)

    player = Sprite(str(base_dir / "src" / "assets" / "images" / "player.png"))
    player.x = player.width
    player.y = (window.height / 2) - (player.height / 2)

    enemy = Sprite(str(base_dir / "src" / "assets" / "images" / "enemy.png"))
    enemy.x = (window.width - 2 * enemy.width)
    enemy.y = (window.height / 2) - (enemy.height / 2)

    vx = 0.25
    vy = 0.25

    # Game Loop
    while is_running:
        window.set_background_color("#0000FF")

        if keyboard.key_pressed("ESC"):
            is_running = False
            window.close()

        move_ball(ball, vx, vy)
        vx, vy = change_directions(window, ball, vx, vy)

        # Renderer
        player.draw()
        enemy.draw()
        ball.draw()

        window.update()

if __name__ == "__main__":
    main()
