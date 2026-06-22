import pygame
from code.Const import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    ROAD_LEFT, ROAD_RIGHT,
    PLAYER_WIDTH, PLAYER_HEIGHT,
    PLAYER_MIN_SPEED, PLAYER_MAX_SPEED
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill((30, 144, 255))  # Azul dodger blue

        # Faróis dianteiros (amarelo claro)
        pygame.draw.rect(self.image, (255, 255, 200), (8, 5, 12, 15))
        pygame.draw.rect(self.image, (255, 255, 200), (30, 5, 12, 15))

        # Para-brisa (cinza claro)
        pygame.draw.rect(self.image, (200, 200, 200), (10, 30, 30, 20))

        # Farol traseiro (vermelho) - detalhe
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