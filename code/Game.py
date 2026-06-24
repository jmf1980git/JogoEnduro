import pygame
import sys
import random
from code.Const import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    ROAD_LEFT, ROAD_RIGHT, LANE_WIDTH, LANE_CENTERS, NUM_LANES,
    C_WHITE, C_RED, C_YELLOW, C_GREEN, C_BLUE, C_ORANGE, C_BLACK, C_GRAY, C_DARK_GRAY,
    PLAYER_WIDTH, PLAYER_HEIGHT,
    ENEMY_BASE_SPEED, ENEMY_SPAWN_INTERVAL, ENEMY_MAX_SPEED,
    LEVEL_BASE_DODGES, LEVEL_DODGE_INCREMENT,
    DIFFICULTY_OPTIONS, DIFFICULTY_NAMES,
    POINTS_PER_ENEMY, PLAYER_LIVES,
    LEVEL_SPEED_INCREMENT, LEVEL_SPAWN_REDUCTION, MIN_SPAWN_INTERVAL,
    BIOMES, BIOME_CHANGE_INTERVAL,
    SCENERY_SPAWN_INTERVAL
)
from code.Player import Player
from code.Enemy import Enemy
from code.Scenery import Scenery
from code.Database import Database
from code.Graphics import Graphics


class Game:
    def __init__(self, window, sound_manager, difficulty):
        self.window = window
        self.sound_manager = sound_manager
        self.clock = pygame.time.Clock()

    # Adicione esta linha
        self.graphics = Graphics()

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

        # Estado do jogo (FASES INFINITAS)
        self.score = 0
        self.lives = PLAYER_LIVES
        self.level = 1
        self.dodged = 0
        self.dodge_target = self._calc_dodge_target(1)
        self.spawn_timer = 0
        self.spawn_interval = max(MIN_SPAWN_INTERVAL, int(ENEMY_SPAWN_INTERVAL * self.diff['spawn_mult']))
        self.scenery_timer = 0
        self.road_offset = 0
        self.running = True
        self.game_over = False
        self.engine_playing = False

        # Sistema de input de nome (top 10)
        self.entering_name = False
        self.player_name = ""
        self.name_saved = False
        self.is_top_score = False

        # Sistema de biomas dinâmicos
        self.biome_timer = 0
        self.current_biome = random.choice(BIOMES)
        self.next_biome = None
        self.transitioning = False
        self.transition_progress = 0.0
        self.transition_speed = 0.02

        # Parar música do menu e iniciar música do jogo
        self.sound_manager.stop_music()
        self.sound_manager.start_game_music()

        # Iniciar som do motor automaticamente
        self.sound_manager.play_sfx('engine', volume=0.3, loops=-1)
        self.engine_playing = True

        # Fontes
        self.font_hud = pygame.font.SysFont("Lucida Sans Typewriter", 20)
        self.font_big = pygame.font.SysFont("Lucida Sans Typewriter", 48, bold=True)
        self.font_medium = pygame.font.SysFont("Lucida Sans Typewriter", 28, bold=True)
        self.font_input = pygame.font.SysFont("Lucida Sans Typewriter", 32)

    def _calc_dodge_target(self, level):
        """Calcula quantos desvios são necessários para passar o nível atual."""
        return LEVEL_BASE_DODGES + (level - 1) * LEVEL_DODGE_INCREMENT

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        # Quando sair do loop
        self.sound_manager.stop_sfx('engine')
        self.sound_manager.stop_music()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Se está digitando o nome
                if self.entering_name:
                    self._handle_name_input(event)
                    return

                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.game_over and self.name_saved:
                    if event.key == pygame.K_r or event.key == pygame.K_RETURN:
                        self._restart()

    def _handle_name_input(self, event):
        """Gerencia a digitação do nome do jogador."""
        if event.key == pygame.K_RETURN:
            # Confirmar nome
            if len(self.player_name) > 0:
                db = Database()
                db.add_record(self.player_name, self.score, self.level, self.difficulty_name)
                self.entering_name = False
                self.name_saved = True
        elif event.key == pygame.K_BACKSPACE:
            # Apagar último caractere
            self.player_name = self.player_name[:-1]
        elif event.key == pygame.K_ESCAPE:
            # Cancelar (salva como "???")
            db = Database()
            db.add_record("???", self.score, self.level, self.difficulty_name)
            self.entering_name = False
            self.name_saved = True
        else:
            # Adicionar caractere (máximo 8)
            if len(self.player_name) < 8 and event.unicode.isprintable() and event.unicode != '':
                self.player_name += event.unicode.upper()

    def _trigger_game_over(self):
        """Ativa o game over e verifica se entrou no top 10."""
        self.sound_manager.stop_sfx('engine')
        self.engine_playing = False
        self.sound_manager.stop_music()
        self.sound_manager.play_sfx('game_over')
        self.game_over = True

        # Verificar se entrou no top 10
        db = Database()
        if db.is_top_score(self.score):
            self.is_top_score = True
            self.entering_name = True
            self.player_name = ""
        else:
            self.is_top_score = False
            self.name_saved = True  # Não precisa salvar nome

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
        self.dodge_target = self._calc_dodge_target(1)
        self.spawn_timer = 0
        self.scenery_timer = 0
        self.spawn_interval = max(MIN_SPAWN_INTERVAL, int(ENEMY_SPAWN_INTERVAL * self.diff['spawn_mult']))
        self.road_offset = 0
        self.game_over = False
        self.engine_playing = False

        # Reset nome
        self.entering_name = False
        self.player_name = ""
        self.name_saved = False
        self.is_top_score = False

        # Reset bioma
        self.biome_timer = 0
        self.current_biome = random.choice(BIOMES)
        self.next_biome = None
        self.transitioning = False
        self.transition_progress = 0.0

        # Reiniciar música e som do motor
        self.sound_manager.stop_music()
        self.sound_manager.start_game_music()
        self.sound_manager.play_sfx('engine', volume=0.3, loops=-1)
        self.engine_playing = True

    def _get_enemy_speed(self):
        """Velocidade dos inimigos aumenta a cada nível, com teto máximo."""
        speed = ENEMY_BASE_SPEED * self.diff['enemy_speed_mult']
        speed += (self.level - 1) * LEVEL_SPEED_INCREMENT
        return min(ENEMY_MAX_SPEED, max(3, speed))

    def _get_spawn_interval(self):
        """Intervalo entre spawns diminui a cada nível (mais carros)."""
        interval = int(ENEMY_SPAWN_INTERVAL * self.diff['spawn_mult'])
        interval -= (self.level - 1) * LEVEL_SPAWN_REDUCTION
        return max(MIN_SPAWN_INTERVAL, interval)

    def _get_simultaneous_spawns(self):
        """Retorna quantos carros podem spawnar ao mesmo tempo baseado no nível."""
        if self.level <= 2:
            return 1
        elif self.level <= 4:
            return random.choice([1, 1, 2])
        elif self.level <= 6:
            return random.choice([1, 2, 2])
        elif self.level <= 8:
            return random.choice([1, 2, 2, 3])
        elif self.level <= 10:
            return random.choice([2, 2, 3, 3])
        else:
            return random.choice([2, 3, 3, min(4, NUM_LANES)])

    def _lerp_color(self, color1, color2, t):
        """Interpola entre duas cores (transição suave)."""
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

    def _update_biome(self):
        """Gerencia a troca dinâmica de biomas."""
        self.biome_timer += 1

        if self.transitioning:
            self.transition_progress += self.transition_speed
            if self.transition_progress >= 1.0:
                self.transition_progress = 1.0
                self.current_biome = self.next_biome
                self.next_biome = None
                self.transitioning = False
                self.biome_timer = 0
        else:
            if self.biome_timer >= BIOME_CHANGE_INTERVAL:
                available = [b for b in BIOMES if b['name'] != self.current_biome['name']]
                self.next_biome = random.choice(available)
                self.transitioning = True
                self.transition_progress = 0.0

    def _get_current_color(self, color_key):
        """Retorna a cor atual considerando a transição entre biomas."""
        if self.transitioning and self.next_biome:
            return self._lerp_color(
                self.current_biome[color_key],
                self.next_biome[color_key],
                self.transition_progress
            )
        return self.current_biome[color_key]

    def _get_current_lane_style(self):
        """Retorna o estilo de faixa atual."""
        if self.transitioning and self.next_biome:
            if self.transition_progress >= 0.5:
                return self.next_biome['lane_style']
        return self.current_biome['lane_style']

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Atualizar sistema de biomas
        self._update_biome()

        # Spawn de inimigos
        self.spawn_timer += 1
        if self.spawn_timer >= self._get_spawn_interval():
            self.spawn_timer = 0
            num_spawns = self._get_simultaneous_spawns()

            available_lanes = list(range(NUM_LANES))
            for _ in range(min(num_spawns, len(available_lanes))):
                if not available_lanes:
                    break
                lane_idx = random.choice(available_lanes)
                available_lanes.remove(lane_idx)
                enemy_speed = self._get_enemy_speed()
                variation_range = min(2.0, 0.5 + self.level * 0.15)
                speed_variation = random.uniform(-0.5, variation_range)
                enemy = Enemy(LANE_CENTERS[lane_idx], -PLAYER_HEIGHT, enemy_speed + speed_variation)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

        # Spawn de objetos de cenário nas laterais
        self.scenery_timer += 1
        if self.scenery_timer >= SCENERY_SPAWN_INTERVAL:
            self.scenery_timer = 0
            side = random.choice(['left', 'right'])
            scenery_obj = Scenery(side, self.player.get_speed())
            self.scenery_objects.add(scenery_obj)

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
                self._trigger_game_over()
                return

        # Verificar inimigos que passaram (dodge)
        for enemy in list(self.enemies):
            if not enemy.counted and enemy.rect.top > self.player.rect.bottom:
                enemy.counted = True
                self.dodged += 1
                points = int(POINTS_PER_ENEMY * self.diff['score_mult'])
                self.score += points
                self.sound_manager.play_sfx('dodge')

        # Verificar progressão de nível (INFINITO)
        if self.dodged >= self.dodge_target:
            self.level += 1
            self.dodged = 0
            self.dodge_target = self._calc_dodge_target(self.level)
            self.sound_manager.play_sfx('level_up')

        # Animação da estrada
        self.road_offset = (self.road_offset + self.player.get_speed()) % 80

    def draw_background(self):
        grass_color = self._get_current_color('grass_color')
        self.window.fill(grass_color)

        road_color = self._get_current_color('road_color')
        road_rect = pygame.Rect(ROAD_LEFT - 10, 0, ROAD_RIGHT - ROAD_LEFT + 20, WINDOW_HEIGHT)
        pygame.draw.rect(self.window, road_color, road_rect)

        border_color = self._get_current_color('border_color')
        pygame.draw.rect(self.window, border_color, (ROAD_LEFT - 5, 0, 5, WINDOW_HEIGHT))
        pygame.draw.rect(self.window, border_color, (ROAD_RIGHT, 0, 5, WINDOW_HEIGHT))

        lane_color = self._get_current_color('lane_color')
        lane_style = self._get_current_lane_style()

        for lane in range(1, NUM_LANES):
            x = ROAD_LEFT + lane * LANE_WIDTH - 2

            if lane_style == 'dashed':
                for y in range(-40, WINDOW_HEIGHT, 80):
                    y_pos = y + self.road_offset
                    pygame.draw.rect(self.window, lane_color, (x, y_pos, 4, 40))
            else:
                pygame.draw.rect(self.window, lane_color, (x, 0, 4, WINDOW_HEIGHT))

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

        diff_text = self.font_hud.render(self.difficulty_name, True, C_YELLOW)
        diff_rect = diff_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        self.window.blit(diff_text, diff_rect)

        biome_name = self.current_biome['name']
        if self.transitioning and self.next_biome:
            biome_name = f"{self.current_biome['name']} > {self.next_biome['name']}"
        biome_text = self.font_hud.render(biome_name, True, C_WHITE)
        biome_rect = biome_text.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
        self.window.blit(biome_text, biome_rect)

    def draw_name_input(self):
        """Desenha a tela de input do nome do jogador."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(C_BLACK)
        overlay.set_alpha(200)
        self.window.blit(overlay, (0, 0))

        # Título
        title = self.font_big.render("TOP 10!", True, C_YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.window.blit(title, title_rect)

        # Pontuação
        score_text = self.font_medium.render(f"Pontuacao: {self.score}", True, C_WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 220))
        self.window.blit(score_text, score_rect)

        # Instrução
        instr = self.font_hud.render("Digite seu nome (max 8 caracteres):", True, C_WHITE)
        instr_rect = instr.get_rect(center=(WINDOW_WIDTH // 2, 290))
        self.window.blit(instr, instr_rect)

        # Campo de input com cursor piscante
        name_display = self.player_name
        # Cursor piscante
        if pygame.time.get_ticks() % 1000 < 500:
            name_display += "_"

        # Caixa de input
        input_box = pygame.Rect(WINDOW_WIDTH // 2 - 150, 320, 300, 50)
        pygame.draw.rect(self.window, C_DARK_GRAY, input_box)
        pygame.draw.rect(self.window, C_WHITE, input_box, 2)

        name_surf = self.font_input.render(name_display, True, C_YELLOW)
        name_rect = name_surf.get_rect(center=input_box.center)
        self.window.blit(name_surf, name_rect)

        # Contador de caracteres
        counter = self.font_hud.render(f"{len(self.player_name)}/8", True, C_GRAY)
        counter_rect = counter.get_rect(center=(WINDOW_WIDTH // 2, 390))
        self.window.blit(counter, counter_rect)

        # Instrução de confirmação
        confirm = self.font_hud.render("ENTER para confirmar | ESC para pular", True, C_GRAY)
        confirm_rect = confirm.get_rect(center=(WINDOW_WIDTH // 2, 440))
        self.window.blit(confirm, confirm_rect)

    def draw_game_over(self):
        """Desenha a tela de game over (após salvar o nome)."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(C_BLACK)
        overlay.set_alpha(180)
        self.window.blit(overlay, (0, 0))

        lines = [
            ("GAME OVER", C_RED, self.font_big),
            (f"Pontuacao: {self.score}", C_WHITE, self.font_medium),
            (f"Nivel alcancado: {self.level}", C_YELLOW, self.font_hud),
        ]

        if self.is_top_score and self.player_name:
            lines.append((f"Parabens, {self.player_name}! Top 10!", C_GREEN, self.font_hud))

        lines.append(("", C_BLACK, self.font_hud))
        lines.append(("Pressione R ou ENTER para reiniciar", C_WHITE, self.font_hud))
        lines.append(("Pressione ESC para sair", C_GRAY, self.font_hud))

        total_h = len(lines) * 45
        start_y = (WINDOW_HEIGHT - total_h) // 2

        for i, (text, color, font) in enumerate(lines):
            if text:
                surf = font.render(text, True, color)
                rect = surf.get_rect(center=(WINDOW_WIDTH // 2, start_y + i * 45))
                self.window.blit(surf, rect)

    def draw(self):
        self.draw_background()

        # Desenhar objetos de cenário (atrás dos carros)
        self.scenery_objects.draw(self.window)

        # Desenhar carros (player e inimigos)
        self.all_sprites.draw(self.window)

        self.draw_hud()

        if self.game_over:
            if self.entering_name:
                # Tela de input do nome
                self.draw_name_input()
            elif self.name_saved:
                # Tela de game over final
                self.draw_game_over()

        pygame.display.flip()
