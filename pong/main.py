import os

from PPlay.window import Window
from PPlay.keyboard import Keyboard
from PPlay.sprite import Sprite


def main():
    is_running = True
    
    keyboard = Keyboard()
    window = Window(800, 580)
    window.set_background_color("#0000FF")
    window.set_title("Pong")

    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, "src", "assets", "ball.png")

    ball = Sprite(image_path)
    ball.set_position(((window.width / 2) - ball.width), (window.height / 2) - ball.height)

    # Game Loop
    while is_running:
        if keyboard.key_pressed("ESC"):
            is_running = False
            window.close()

        ball.draw()
        window.update()

if __name__ == "__main__":
    main()