from pathlib import Path
from random import choice, uniform

from pplay.window import Window
from pplay.keyboard import Keyboard
from pplay.sprite import Sprite

base_dir = Path(__file__).resolve().parent

MAX_SPEED = 1200
SPEED_FACTOR = 1.08

PADDLE_SPEED = 500

AI_SPEED = 280
AI_DEAD_ZONE = 12

INITIAL_BALL_SPEED_X = 420
INITIAL_BALL_SPEED_Y = 240


def check_colision(a, b):
    return a.collided(b)


def move_ball(ball, dt, vx, vy):
    ball.x += vx * dt
    ball.y += vy * dt


def move_player(keyboard, player, dt):
    if keyboard.key_pressed("UP"):
        player.y -= PADDLE_SPEED * dt
    if keyboard.key_pressed("DOWN"):
        player.y += PADDLE_SPEED * dt


def move_enemy(enemy, ball, window, dt, vx):    
    if vx > 0:
        target_y = ball.y + (ball.height / 2)
    else:
        target_y = window.height / 2

    enemy_center = enemy.y + (enemy.height / 2)
    diff = target_y - enemy_center

    if abs(diff) <= AI_DEAD_ZONE:
        return

    direction = 1 if diff > 0 else -1
    enemy.y += direction * AI_SPEED * dt


def keep_paddle_inside_window(paddle, window):
    if paddle.y < 0:
        paddle.y = 0
    elif (paddle.y + paddle.height) > window.height:
        paddle.y = window.height - paddle.height


def speed_up(value, factor = SPEED_FACTOR, max_speed = MAX_SPEED):
    direction = -1 if value < 0 else 1
    new_speed = min(abs(value) * factor, max_speed)
    return direction * new_speed


def bounce_on_top_bottom(window, ball, vy):
    if ball.y <= 0:
        ball.y = 0
        vy = abs(vy)
    elif (ball.y + ball.height) >= window.height:
        ball.y = window.height - ball.height
        vy = -abs(vy)

    return vy


def handle_paddle_collision(ball, player, enemy, vx, vy):
    if vx < 0 and check_colision(ball, player):
        ball.x = player.x + player.width
        vx = abs(speed_up(vx))

        hit_pos = ((ball.y + ball.height / 2) - (player.y + player.height / 2))
        normalized = hit_pos / (player.height / 2)
        vy += normalized * 180

    if vx > 0 and check_colision(ball, enemy):
        ball.x = enemy.x - ball.width
        vx = -abs(speed_up(vx))
        hit_pos = ((ball.y + ball.height / 2) - (enemy.y + enemy.height / 2))
        normalized = hit_pos / (enemy.height / 2)
        vy += normalized * 180

    vy = max(-MAX_SPEED, min(vy, MAX_SPEED))

    return vx, vy


def reset_enemy(enemy, window):
    enemy.x = (window.width - 2 * enemy.width)
    enemy.y = (window.height / 2) - (enemy.height / 2)


def reset_player(player, window):
    player.x = player.width
    player.y = (window.height / 2) - (player.height / 2)


def reset_ball(ball, window):
    ball.x = (window.width / 2) - (ball.width / 2)
    ball.y = (window.height / 2) - (ball.height / 2)


def reset_pos(a, b, c, window):
    reset_player(a, window)
    reset_enemy(b, window)
    reset_ball(c, window)


def initial_ball_velocity():
    vx = INITIAL_BALL_SPEED_X * choice((-1, 1))
    vy = INITIAL_BALL_SPEED_Y * uniform(-1.0, 1.0)
    return vx, vy


def main():
    # Variáveis
    is_running = True
    waiting_start = True
    
    player_score = 0
    enemy_score = 0
    
    # Objetos
    window = Window(800, 600)
    window.set_title("Pong")

    keyboard = Keyboard()

    ball = Sprite(str(base_dir / "src" / "assets" / "images" / "ball.png"))
    reset_ball(ball, window)

    player = Sprite(str(base_dir / "src" / "assets" / "images" / "player.png"))
    reset_player(player, window)

    enemy = Sprite(str(base_dir / "src" / "assets" / "images" / "enemy.png"))
    reset_enemy(enemy, window)

    vx, vy = initial_ball_velocity()

    # Game Loop
    while is_running:
        window.set_background_color([42, 195, 36])
        dt = window.delta_time()

        if keyboard.key_pressed("ESC"):
            is_running = False
            window.close()

        if not waiting_start:
            move_player(keyboard, player, dt)
        move_enemy(enemy, ball, window, dt, vx)

        keep_paddle_inside_window(player, window)
        keep_paddle_inside_window(enemy, window)

        if not waiting_start:
            move_ball(ball, dt, vx, vy)
            vy = bounce_on_top_bottom(window, ball, vy)
            vx, vy = handle_paddle_collision(ball, player, enemy, vx, vy)

            if (ball.x + ball.width) < 0:
                enemy_score += 1
                reset_pos(player, enemy, ball, window)
                vx, vy = initial_ball_velocity()
                waiting_start = True
            elif ball.x > window.width:
                player_score += 1
                reset_pos(player, enemy, ball, window)
                vx, vy = initial_ball_velocity()
                waiting_start = True

        score_text = f"{player_score}   X   {enemy_score}"
        window.draw_text(score_text, (window.width / 2) - 45, 20, size=34, color=(255, 255, 255), bold=True)

        if waiting_start:
            if keyboard.key_pressed("SPACE"):
                waiting_start = False

        # Renderer
        player.draw()
        enemy.draw()
        ball.draw()

        window.update()

if __name__ == "__main__":
    main()
