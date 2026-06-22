import pygame
import os


class SoundManager:
    SOUND_PATH = './asset/sound/'

    SFX_FILES = {
        'menu_move': 'menu_move.wav',
        'menu_select': 'menu_select.wav',
        'engine': 'car_move.mp3',
        'dodge': 'dodge.wav',
        'crash': 'crash.wav',
        'level_up': 'leveUp.mp3',
        'game_over': 'game_over.wav',
        'victory': 'victory.wav',
    }

    def __init__(self):
        pygame.mixer.init()
        self.sound = {}
        for name, filename in self.SFX_FILES.items():
            try:
                path = os.path.join(self.SOUND_PATH, filename)
                if os.path.exists(path):
                    self.sound[name] = pygame.mixer.Sound(path)
                else:
                    self.sound[name] = None
            except Exception:
                self.sound[name] = None

    def play_sfx(self, name, volume=1.0, loops=0):
        sound = self.sound.get(name)
        if sound is not None:
            sound.set_volume(volume)
            sound.play(loops=loops)

    def stop_sfx(self, name):
        sound = self.sound.get(name)
        if sound is not None:
            sound.stop()

    def start_menu_music(self):
        """Inicia a música de fundo do menu."""
        try:
            path = os.path.join(self.SOUND_PATH, 'menu_music.mp3')
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
        except Exception:
            pass

    def start_game_music(self):
        """Inicia a música de fundo durante o jogo."""
        try:
            path = os.path.join(self.SOUND_PATH, 'speed1.mp3')
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
        except Exception:
            pass

    def stop_music(self):
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception:
            pass
