from PPlay.window import *
from PPlay.keyboard import *


def main():
    is_running = True
    
    keyboard = Keyboard()
    window = Window(800, 580)
    window.set_background_color("#0000FF")
    window.set_title("Hello World")

    while is_running:
        if keyboard.key_pressed("ESC"):
            is_running = False
            window.close()

        window.update()

if __name__ == "__main__":
    main()
