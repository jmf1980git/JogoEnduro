"""
Graphics.py - Sistema de Renderização do Jogo Enduro 2D
Copie este arquivo para a pasta 'code/' do seu projeto
Renomeie para 'Graphics.py' (sem o '_Corrigido_v2')
"""

import pygame
from code.Const import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    C_WHITE, C_BLACK, C_YELLOW, C_RED, C_GREEN, C_BLUE, C_ORANGE, C_GRAY, C_DARK_GRAY
)


class Graphics:
    """Gerenciador de renderização com HUD horizontal e background preto."""
    
    def __init__(self):
        """Inicializa o sistema de gráficos."""
        self.font_hud = pygame.font.SysFont("Lucida Sans Typewriter", 18, bold=True)
        self.font_hud_small = pygame.font.SysFont("Lucida Sans Typewriter", 14)
        self.hud_height = 50  # Altura da barra HUD superior
        
    def draw_hud(self, window, player, level, dodged, dodge_target, score, lives, 
                 difficulty_name, current_biome, next_biome=None, transitioning=False):
        """
        Desenha a HUD completa com todas as informações.
        
        Args:
            window: Surface do pygame
            player: Objeto do jogador
            level: Nível atual
            dodged: Quantidade de desvios realizados
            dodge_target: Alvo de desvios para passar de nível
            score: Pontuação atual
            lives: Vidas restantes
            difficulty_name: Nome da dificuldade
            current_biome: Dicionário do bioma atual
            next_biome: Dicionário do próximo bioma (se em transição)
            transitioning: Se está em transição de bioma
        """
        # ========== BARRA SUPERIOR (HUD Horizontal) ==========
        # Background preto
        pygame.draw.rect(window, C_BLACK, (0, 0, WINDOW_WIDTH, self.hud_height))
        
        # Borda amarela inferior (usando rect com width=2)
        pygame.draw.rect(window, C_YELLOW, (0, self.hud_height - 2, WINDOW_WIDTH, 2))
        
        # Posições e espaçamento
        y_text = 12  # Posição vertical do texto
        x_start = 15  # Posição inicial horizontal
        spacing = 180  # Espaço entre cada informação
        
        # 1. SCORE (Amarelo)
        score_text = self.font_hud.render(f"SCORE: {score}", True, C_YELLOW)
        window.blit(score_text, (x_start, y_text))
        
        # 2. VIDAS (Branco)
        x_start += spacing
        lives_text = self.font_hud.render(f"VIDAS: {lives}", True, C_WHITE)
        window.blit(lives_text, (x_start, y_text))
        
        # 3. NIVEL (Cor dinâmica baseada na dificuldade)
        x_start += spacing
        nivel_color = self._get_difficulty_color(difficulty_name)
        nivel_text = self.font_hud.render(f"NIVEL: {level}", True, nivel_color)
        window.blit(nivel_text, (x_start, y_text))
        
        # 4. VEL (Branco)
        x_start += spacing
        vel_text = self.font_hud.render(f"VEL: {player.get_speed()}", True, C_WHITE)
        window.blit(vel_text, (x_start, y_text))
        
        # 5. DESV (Branco)
        x_start += spacing
        desv_text = self.font_hud.render(f"DESV: {dodged}/{dodge_target}", True, C_WHITE)
        window.blit(desv_text, (x_start, y_text))
        
        # ========== INFORMAÇÕES LATERAIS ==========
        # Dificuldade (canto superior direito)
        diff_text = self.font_hud.render(difficulty_name, True, C_YELLOW)
        diff_rect = diff_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        window.blit(diff_text, diff_rect)
        
        # Bioma (canto inferior direito)
        biome_name = current_biome['name'] if current_biome else "Desconhecido"
        if transitioning and next_biome:
            biome_name = f"{current_biome['name']} > {next_biome['name']}"
        
        biome_text = self.font_hud.render(biome_name, True, C_WHITE)
        biome_rect = biome_text.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
        window.blit(biome_text, biome_rect)
    
    def _get_difficulty_color(self, difficulty):
        """
        Retorna a cor baseada na dificuldade.
        
        Args:
            difficulty: Nome da dificuldade
            
        Returns:
            Tupla RGB da cor
        """
        difficulty_colors = {
            "Fácil": C_GREEN,
            "Normal": C_YELLOW,
            "Difícil": C_ORANGE,
            "Extremo": C_RED
        }
        return difficulty_colors.get(difficulty, C_WHITE)
    
    def draw_game_over_screen(self, window, score, level, difficulty):
        """Desenha a tela de game over."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(C_BLACK)
        window.blit(overlay, (0, 0))
        
        font_title = pygame.font.SysFont("Lucida Sans Typewriter", 60, bold=True)
        title = font_title.render("GAME OVER", True, C_RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        window.blit(title, title_rect)
        
        font_info = pygame.font.SysFont("Lucida Sans Typewriter", 28)
        
        score_text = font_info.render(f"PONTUAÇÃO: {score}", True, C_YELLOW)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        window.blit(score_text, score_rect)
        
        level_text = font_info.render(f"NÍVEL: {level}", True, C_YELLOW)
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, 260))
        window.blit(level_text, level_rect)
        
        diff_color = self._get_difficulty_color(difficulty)
        diff_text = font_info.render(f"DIFICULDADE: {difficulty}", True, diff_color)
        diff_rect = diff_text.get_rect(center=(WINDOW_WIDTH // 2, 320))
        window.blit(diff_text, diff_rect)
        
        font_small = pygame.font.SysFont("Lucida Sans Typewriter", 18)
        instr = font_small.render("Pressione R para reiniciar ou ESC para voltar ao menu", True, C_WHITE)
        instr_rect = instr.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        window.blit(instr, instr_rect)
    
    def draw_name_input_screen(self, window, player_name, is_top_score):
        """Desenha a tela de entrada de nome para recordes."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(C_BLACK)
        window.blit(overlay, (0, 0))
        
        font_title = pygame.font.SysFont("Lucida Sans Typewriter", 40, bold=True)
        font_text = pygame.font.SysFont("Lucida Sans Typewriter", 28)
        
        if is_top_score:
            title = font_title.render("NOVO RECORDE!", True, C_YELLOW)
        else:
            title = font_title.render("Digite seu nome", True, C_WHITE)
        
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        window.blit(title, title_rect)
        
        input_text = font_text.render(player_name + "_", True, C_YELLOW)
        input_rect = input_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        window.blit(input_text, input_rect)
        
        font_small = pygame.font.SysFont("Lucida Sans Typewriter", 18)
        instr = font_small.render("ENTER para confirmar | ESC para cancelar (máx 8 caracteres)", True, C_WHITE)
        instr_rect = instr.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        window.blit(instr, instr_rect)
    
    def draw_pause_screen(self, window):
        """Desenha a tela de pausa."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(C_BLACK)
        window.blit(overlay, (0, 0))
        
        font_title = pygame.font.SysFont("Lucida Sans Typewriter", 60, bold=True)
        font_text = pygame.font.SysFont("Lucida Sans Typewriter", 24)
        
        title = font_title.render("PAUSA", True, C_YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 200))
        window.blit(title, title_rect)
        
        instr = font_text.render("Pressione P para continuar", True, C_WHITE)
        instr_rect = instr.get_rect(center=(WINDOW_WIDTH // 2, 300))
        window.blit(instr, instr_rect)
