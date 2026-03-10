from PPlay.window import Window
from PPlay.keyboard import Keyboard


def main():
    is_running = True
    
    keyboard = Keyboard()
    window = Window(800, 580)
    window.set_background_color("#FF0000")
    window.set_title("Hello World")

    while is_running:
        if keyboard.key_pressed("ESC"):
            is_running = False
            window.close()

        window.update()
        window.draw_text("Hello World", window.get_screen().get_width() / 2, window.get_screen().get_height() / 2, 24, (255,255,255))

if __name__ == "__main__":
    main()
