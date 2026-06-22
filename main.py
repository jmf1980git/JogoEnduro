import pygame
import sys
from code.Const import WINDOW_WIDTH, WINDOW_HEIGHT
from code.Menu import Menu
from code.Game import Game
from code.SoundManager import SoundManager


def main():
    pygame.init()
    pygame.mixer.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Enduro 2D")
    sound_manager = SoundManager()

    while True:
        menu = Menu(window, sound_manager)
        choice, difficulty = menu.run()

        if choice == "JOGAR":
            sound_manager.stop_music()
            game = Game(window, sound_manager, difficulty)
            game.run()
        elif choice == "SAIR":
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()