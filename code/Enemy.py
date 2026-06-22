import pygame
import os
from code.Const import WINDOW_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT


class Enemy(pygame.sprite.Sprite):
    PICTURE_PATH = './asset/picture/'

    def __init__(self, centerx, y, speed):
        super().__init__()

        # Tenta carregar imagem do carro inimigo, senão desenha programaticamente
        img_path = os.path.join(self.PICTURE_PATH, 'enemy_car.png')
        if os.path.exists(img_path):
            self.image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
        else:
            # Fallback: desenho programático (caso a imagem não exista)
            self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
            self.image.fill((220, 20, 60))
            pygame.draw.rect(self.image, (255, 0, 0), (8, 72, 12, 8))
            pygame.draw.rect(self.image, (255, 0, 0), (30, 72, 12, 8))
            pygame.draw.rect(self.image, (70, 130, 180), (10, 10, 30, 20))

        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = y
        self.speed = speed
        self.counted = False

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
