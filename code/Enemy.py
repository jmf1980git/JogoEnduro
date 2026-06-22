import pygame
from code.Const import WINDOW_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self, centerx, y, speed):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill((220, 20, 60))  # Vermelho

        # Faróis traseiros
        pygame.draw.rect(self.image, (255, 0, 0), (8, 72, 12, 8))
        pygame.draw.rect(self.image, (255, 0, 0), (30, 72, 12, 8))

        # Vidro traseiro
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