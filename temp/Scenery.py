import pygame
import os
import random
from code.Const import (
    WINDOW_HEIGHT, ROAD_LEFT, ROAD_RIGHT, WINDOW_WIDTH,
    SCENERY_SPEED_MULT, SCENERY_SPAWN_INTERVAL,
    SCENERY_OBJECTS
)


class Scenery(pygame.sprite.Sprite):
    """Objeto de cenário lateral (árvores, pessoas, animais).
    Aparece nas laterais da estrada e se move para baixo simulando movimento."""

    PICTURE_PATH = './asset/picture/'

    def __init__(self, side, player_speed):
        super().__init__()

        # Escolher aleatoriamente um tipo de objeto e uma variação
        obj_type = random.choice(list(SCENERY_OBJECTS.keys()))
        obj_info = SCENERY_OBJECTS[obj_type]
        variation = random.choice(obj_info['files'])

        # Tamanho do objeto
        self.width = obj_info['width']
        self.height = obj_info['height']

        # Tenta carregar a imagem, senão usa fallback colorido
        img_path = os.path.join(self.PICTURE_PATH, variation)
        if os.path.exists(img_path):
            self.image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        else:
            # Fallback: retângulo colorido
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            color = obj_info.get('fallback_color', (0, 200, 0))
            self.image.fill(color)

        self.rect = self.image.get_rect()

        # Posicionar no lado correto (esquerda ou direita da estrada)
        if side == 'left':
            # Área esquerda: entre 0 e a borda esquerda da estrada
            margin = 20
            max_x = ROAD_LEFT - self.width - 10
            if max_x < margin:
                max_x = margin
            self.rect.x = random.randint(margin, max_x)
        else:
            # Área direita: entre a borda direita da estrada e a borda da tela
            min_x = ROAD_RIGHT + 10
            max_x = WINDOW_WIDTH - self.width - 10
            if max_x < min_x:
                max_x = min_x
            self.rect.x = random.randint(min_x, max_x)

        # Começar acima da tela
        self.rect.y = -self.height

        # Velocidade proporcional à velocidade do jogador
        self.base_speed = player_speed * SCENERY_SPEED_MULT

    def update(self, player_speed=None):
        """Move o objeto para baixo. Se player_speed for passado, ajusta a velocidade."""
        if player_speed is not None:
            self.base_speed = player_speed * SCENERY_SPEED_MULT

        self.rect.y += self.base_speed

        # Remover quando sair da tela
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
