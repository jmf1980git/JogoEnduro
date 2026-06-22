import pygame
import os
from code.Const import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    ROAD_LEFT, ROAD_RIGHT,
    PLAYER_WIDTH, PLAYER_HEIGHT,
    PLAYER_MIN_SPEED, PLAYER_MAX_SPEED
)


class Player(pygame.sprite.Sprite):
    PICTURE_PATH = './asset/picture/'

    def __init__(self):
        super().__init__()

        # Tenta carregar imagem do carro, senão desenha programaticamente
        img_path = os.path.join(self.PICTURE_PATH, 'player_car.png')
        if os.path.exists(img_path):
            self.image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        else:
            # Fallback: desenho programático (caso a imagem não exista)
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill((30, 144, 255))
            pygame.draw.rect(self.image, (255, 255, 200), (8, 5, 12, 15))
            pygame.draw.rect(self.image, (255, 255, 200), (30, 5, 12, 15))
            pygame.draw.rect(self.image, (200, 200, 200), (10, 30, 30, 20))
            pygame.draw.rect(self.image, (255, 50, 50), (8, 72, 12, 8))
            pygame.draw.rect(self.image, (255, 50, 50), (30, 72, 12, 8))

        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 20

        self.speed = PLAYER_MIN_SPEED
        self.min_speed = PLAYER_MIN_SPEED
        self.max_speed = PLAYER_MAX_SPEED
        self.lateral_speed = 7

    def update(self, keys):
        # Acelerar / desacelerar com setas cima/baixo
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.speed + 0.5, self.max_speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(self.speed - 0.3, self.min_speed)

        # Movimento lateral com setas esquerda/direita
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.lateral_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.lateral_speed

        # Limitar dentro da estrada
        if self.rect.left < ROAD_LEFT:
            self.rect.left = ROAD_LEFT
        if self.rect.right > ROAD_RIGHT:
            self.rect.right = ROAD_RIGHT

    def is_accelerating(self):
        return self.speed > self.min_speed + 0.5

    def get_speed(self):
        return int(self.speed)
