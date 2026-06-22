import pygame
import os
import random
from code.Const import WINDOW_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_CAR_FILES


class Enemy(pygame.sprite.Sprite):
    """Carro inimigo com múltiplos modelos visuais escolhidos aleatoriamente."""

    PICTURE_PATH = './asset/picture/'

    # Cache de imagens carregadas (compartilhado entre instâncias)
    _image_cache = {}

    def __init__(self, centerx, y, speed):
        super().__init__()

        # Escolher aleatoriamente um modelo de carro inimigo
        car_file = random.choice(ENEMY_CAR_FILES)

        # Verificar cache para não recarregar a mesma imagem
        if car_file in Enemy._image_cache:
            self.image = Enemy._image_cache[car_file].copy()
        else:
            img_path = os.path.join(self.PICTURE_PATH, car_file)
            if os.path.exists(img_path):
                loaded = pygame.image.load(img_path).convert_alpha()
                loaded = pygame.transform.scale(loaded, (ENEMY_WIDTH, ENEMY_HEIGHT))
                Enemy._image_cache[car_file] = loaded
                self.image = loaded.copy()
            else:
                # Fallback: desenho programático com cores aleatórias
                self.image = self._create_fallback_car()

        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = y
        self.speed = speed
        self.counted = False

    def _create_fallback_car(self):
        """Cria um carro desenhado programaticamente com cor aleatória."""
        colors = [
            (220, 20, 60),    # Vermelho
            (255, 140, 0),    # Laranja
            (148, 0, 211),    # Roxo
            (0, 100, 0),      # Verde escuro
            (25, 25, 112),    # Azul marinho
            (139, 69, 19),    # Marrom
        ]
        car_color = random.choice(colors)

        image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
        image.fill(car_color)

        # Faróis traseiros
        pygame.draw.rect(image, (255, 0, 0), (8, 72, 12, 8))
        pygame.draw.rect(image, (255, 0, 0), (30, 72, 12, 8))

        # Vidro traseiro
        pygame.draw.rect(image, (70, 130, 180), (10, 10, 30, 20))

        return image

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
