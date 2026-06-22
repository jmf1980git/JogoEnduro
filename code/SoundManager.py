import pygame
import os


class SoundManager:
    SOUND_PATH = './asset/sounds/'

    SFX_FILES = {
        'menu_move': 'menu_move.wav',
        'menu_select': 'menu_select.wav',
        'engine': 'engine.wav',
        'dodge': 'dodge.wav',
        'crash': 'crash.wav',
        'level_up': 'level_up.wav',
        'game_over': 'game_over.wav',
        'victory': 'victory.wav',
    }

    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        for name, filename in self.SFX_FILES.items():
            try:
                path = os.path.join(self.SOUND_PATH, filename)
                self.sounds[name] = pygame.mixer.Sound(path)
            except Exception:
                self.sounds[name] = None

    def play_sfx(self, name, volume=1.0, loops=0):
        sound = self.sounds.get(name)
        if sound is not None:
            sound.set_volume(volume)
            sound.play(loops=loops)

    def stop_sfx(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            sound.stop()

    def start_menu_music(self):
        try:
            path = os.path.join(self.SOUND_PATH, 'menu_music.ogg')
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
        except Exception:
            pass

    def stop_music(self):
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception:
            pass