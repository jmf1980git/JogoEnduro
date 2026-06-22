import pygame
import sys
import os
import atexit


def get_base_path():
    """Retorna o caminho base do projeto.
    Funciona tanto rodando como script (.py) quanto como executável (.exe).
    """
    if getattr(sys, 'frozen', False):
        # Rodando como executável (PyInstaller)
        return sys._MEIPASS
    else:
        # Rodando como script Python
        return os.path.dirname(os.path.abspath(__file__))


# Definir o caminho base ANTES de importar os módulos do jogo
BASE_PATH = get_base_path()
os.chdir(BASE_PATH)

# Adicionar o caminho base ao sys.path para imports funcionarem
if BASE_PATH not in sys.path:
    sys.path.insert(0, BASE_PATH)

from code.Const import WINDOW_WIDTH, WINDOW_HEIGHT
from code.Menu import Menu
from code.Game import Game
from code.SoundManager import SoundManager


def cleanup():
    """Garante que o pygame seja encerrado corretamente."""
    try:
        pygame.mixer.quit()
    except Exception:
        pass
    try:
        pygame.quit()
    except Exception:
        pass


# Registrar cleanup para quando o programa encerrar
atexit.register(cleanup)


def main():
    # Pre-init do mixer para configurar antes da inicialização
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    pygame.mixer.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Enduro 2D")

    sound_manager = SoundManager()

    running = True
    while running:
        try:
            menu = Menu(window, sound_manager)
            choice, difficulty = menu.run()

            if choice == "JOGAR":
                sound_manager.stop_music()
                game = Game(window, sound_manager, difficulty)
                game.run()
            elif choice == "SAIR":
                running = False

        except KeyboardInterrupt:
            running = False
        except SystemExit:
            running = False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            running = False

    cleanup()
    sys.exit()


if __name__ == "__main__":
    main()
