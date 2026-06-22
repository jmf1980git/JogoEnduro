import pygame
import sys
import random
from code.Const import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    ROAD_LEFT, ROAD_RIGHT, LANE_WIDTH, LANE_CENTERS, NUM_LANES,
    C_WHITE, C_RED, C_YELLOW, C_GREEN, C_BLUE, C_ORANGE, C_BLACK, C_GRAY, C_DARK_GRAY,
    PLAYER_WIDTH, PLAYER_HEIGHT,
    ENEMY_BASE_SPEED, ENEMY_SPAWN_INTERVAL,
    LEVEL_ENEMY_COUNTS, DIFFICULTY_OPTIONS, DIFFICULTY_NAMES,
    POINTS_PER_ENEMY, PLAYER_LIVES,
    ROAD_COLOR, ROAD_BORDER_COLOR, ROAD_LANE_COLOR, GRASS_COLOR,
    SCENERY_SPAWN_INTERVAL
)
from code.Player import Player
from code.Enemy import Enemy
from code.Scenery import Scenery
from code.Database import Database


class Game:
    def __init__(self, window, sound_manager, difficulty):
        self.window = window
        self.sound_manager = sound_manager
        self.clock = pygame.time.Clock()

        # Dificuldade: achar o índice pelo nome
        diff_index = 1
        for i, name in enumerate(DIFFICULTY_NAMES):
            if name == difficulty:
                diff_index = i
                break
        self.diff = DIFFICULTY_OPTIONS[diff_index]
        self.difficulty_name = difficulty

        # Player e grupos
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.scenery_objects = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Estado do jogo
        self.score = 0
        self.lives = PLAYER_LIVES
        self.level = 1
        self.dodged = 0
        self.dodge_target = LEVEL_ENEMY_COUNTS[0]
        self.spawn_timer = 0
        self.spawn_interval = max(30, int(ENEMY_SPAWN_INTERVAL * self.diff['spawn_mult']))
        self.scenery_timer = 0
        self.road_offset = 0
        self.running = True
        self.game_over = False
        self.victory = False
        self.engine_playing = False

        # Parar música do menu e iniciar música do jogo
        self.sound_manager.stop_music()
        self.sound_manager.start_game_music()

        # Iniciar som do motor automaticamente
        self.sound_manager.play_sfx('engine', volume=0.3, loops=-1)
        self.engine_playing = True

        # Fontes
        self.font_hud = pygame.font.SysFont("Lucida Sans Typewriter", 20)
        self.font_big = pygame.font.SysFont("Lucida Sans Typewriter", 48, bold=True)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        # Quando sair do loop
        self.sound_manager.stop_sfx('engine')
        self.sound_manager.stop_music()
        if self.game_over or self.victory:
            db = Database()
            db.add_record("Jogador", self.score, self.level, self.difficulty_name)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.game_over or self.victory:
                    if event.key == pygame.K_r or event.key == pygame.K_RETURN:
                        self._restart()

    def _restart(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.scenery_objects = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.score = 0
        self.lives = PLAYER_LIVES
        self.level = 1
        self.dodged = 0
        self.dodge_target = LEVEL_ENEMY_COUNTS[0]
        self.spawn_timer = 0
        self.scenery_timer = 0
        self.spawn_interval = max(30, int(ENEMY_SPAWN_INTERVAL * self.diff['spawn_mult']))
        self.road_offset = 0
        self.game_over = False
        self.victory = False
        self.engine_playing = False

        # Reiniciar música e som do motor
        self.sound_manager.stop_music()
        self.sound_manager.start_game_music()
        self.sound_manager.play_sfx('engine', volume=0.3, loops=-1)
        self.engine_playing = True

    def _get_enemy_speed(self):
        speed = ENEMY_BASE_SPEED * self.diff['enemy_speed_mult']
        speed += (self.level - 1) * 0.5
        return max(2, speed)

    def _get_spawn_interval(self):
        interval = int(ENEMY_SPAWN_INTERVAL * self.diff['spawn_mult'])
        interval -= (self.level - 1) * 5
        return max(20, interval)

    def update(self):
        if self.game_over or self.victory:
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Spawn de inimigos
        self.spawn_timer += 1
        if self.spawn_timer >= self._get_spawn_interval():
            self.spawn_timer = 0
            lane = random.randint(0, NUM_LANES - 1)
            enemy_speed = self._get_enemy_speed()
            enemy = Enemy(LANE_CENTERS[lane], -PLAYER_HEIGHT, enemy_speed)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        # Spawn de objetos de cenário nas laterais
        self.scenery_timer += 1
        if self.scenery_timer >= SCENERY_SPAWN_INTERVAL:
            self.scenery_timer = 0
            # Spawnar em um lado aleatório (ou ambos)
            side = random.choice(['left', 'right'])
            scenery_obj = Scenery(side, self.player.get_speed())
            self.scenery_objects.add(scenery_obj)

            # Chance de spawnar no outro lado também (30%)
            if random.random() < 0.3:
                other_side = 'right' if side == 'left' else 'left'
                scenery_obj2 = Scenery(other_side, self.player.get_speed())
                self.scenery_objects.add(scenery_obj2)

        # Atualizar inimigos
        self.enemies.update()

        # Atualizar objetos de cenário
        for obj in self.scenery_objects:
            obj.update(self.player.get_speed())

        # Colisão
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if hits:
            self.lives -= 1
            self.sound_manager.play_sfx('crash')
            if self.lives <= 0:
                self.sound_manager.stop_sfx('engine')
                self.engine_playing = False
                self.sound_manager.stop_music()
                self.sound_manager.play_sfx('game_over')
                self.game_over = True
                return

        # Verificar inimigos que passaram (dodge)
        for enemy in list(self.enemies):
            if not enemy.counted and enemy.rect.top > self.player.rect.bottom:
                enemy.counted = True
                self.dodged += 1
                points = int(POINTS_PER_ENEMY * self.diff['score_mult'])
                self.score += points
                self.sound_manager.play_sfx('dodge')

        # Verificar progressão de nível
        if self.dodged >= self.dodge_target:
            self.level += 1
            if self.level > len(LEVEL_ENEMY_COUNTS):
                self.sound_manager.play_sfx('victory')
                self.sound_manager.stop_sfx('engine')
                self.engine_playing = False
                self.sound_manager.stop_music()
                self.victory = True
                return
            self.dodged = 0
            self.dodge_target = LEVEL_ENEMY_COUNTS[self.level - 1]
            self.sound_manager.play_sfx('level_up')

        # Animação da estrada
        self.road_offset = (self.road_offset + self.player.get_speed()) % 80

    def draw_background(self):
        # Grama / lateral (cor customizável)
        self.window.fill(GRASS_COLOR)

        # Estrada (cor customizável)
        road_rect = pygame.Rect(ROAD_LEFT - 10, 0, ROAD_RIGHT - ROAD_LEFT + 20, WINDOW_HEIGHT)
        pygame.draw.rect(self.window, ROAD_COLOR, road_rect)

        # Bordas da estrada (cor customizável)
        pygame.draw.rect(self.window, ROAD_BORDER_COLOR, (ROAD_LEFT - 5, 0, 5, WINDOW_HEIGHT))
        pygame.draw.rect(self.window, ROAD_BORDER_COLOR, (ROAD_RIGHT, 0, 5, WINDOW_HEIGHT))

        # Linhas pontilhadas das faixas (cor customizável)
        for lane in range(1, NUM_LANES):
            x = ROAD_LEFT + lane * LANE_WIDTH - 2
            for y in range(-40, WINDOW_HEIGHT, 80):
                y_pos = y + self.road_offset
                pygame.draw.rect(self.window, ROAD_LANE_COLOR, (x, y_pos, 4, 40))

    def draw_hud(self):
        hud_lines = [
            f"SCORE: {self.score}",
            f"VIDAS: {self.lives}",
            f"NIVEL: {self.level}",
            f"VEL:   {self.player.get_speed()}",
            f"DESV:  {self.dodged}/{self.dodge_target}",
        ]
        y = 10
        for line in hud_lines:
            text = self.font_hud.render(line, True, C_WHITE)
            self.window.blit(text, (10, y))
            y += 22

        # Dificuldade no canto superior direito
        diff_text = self.font_hud.render(self.difficulty_name, True, C_YELLOW)
        diff_rect = diff_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        self.window.blit(diff_text, diff_rect)

    def draw_centered_texts(self, lines):
        """Desenha textos centralizados (para Game Over / Vitoria)."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(C_BLACK)
        overlay.set_alpha(180)
        self.window.blit(overlay, (0, 0))

        total_h = len(lines) * 50
        start_y = (WINDOW_HEIGHT - total_h) // 2

        for i, (text, color, font) in enumerate(lines):
            surf = font.render(text, True, color)
            rect = surf.get_rect(center=(WINDOW_WIDTH // 2, start_y + i * 50))
            self.window.blit(surf, rect)

    def draw(self):
        self.draw_background()

        # Desenhar objetos de cenário (atrás dos carros)
        self.scenery_objects.draw(self.window)

        # Desenhar carros (player e inimigos)
        self.all_sprites.draw(self.window)

        self.draw_hud()

        if self.game_over:
            self.draw_centered_texts([
                ("GAME OVER", C_RED, self.font_big),
                (f"Pontuacao: {self.score}", C_WHITE, self.font_hud),
                ("Pressione R ou ENTER para reiniciar", C_WHITE, self.font_hud),
                ("Pressione ESC para sair", C_GRAY, self.font_hud),
            ])
        elif self.victory:
            self.draw_centered_texts([
                ("VITORIA!", C_YELLOW, self.font_big),
                (f"Pontuacao final: {self.score}", C_WHITE, self.font_hud),
                ("Pressione R ou ENTER para reiniciar", C_WHITE, self.font_hud),
                ("Pressione ESC para sair", C_GRAY, self.font_hud),
            ])

        pygame.display.flip()
