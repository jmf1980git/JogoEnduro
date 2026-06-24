import pygame
from code.Const import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    C_WHITE, C_BLACK, C_YELLOW, C_RED, C_GREEN, C_BLUE, C_ORANGE, C_GRAY, C_DARK_GRAY
)


class Graphics:
    """Gerenciador de renderização do jogo com HUD horizontal."""
    
    def __init__(self):
        """Inicializa o sistema de gráficos."""
        self.font_hud = pygame.font.SysFont("Lucida Sans Typewriter", 18, bold=True)
        self.font_hud_small = pygame.font.SysFont("Lucida Sans Typewriter", 14)
        self.hud_height = 50  # Altura da barra de HUD
        
    def draw_hud_horizontal(self, window, player, level, dodged, dodge_target, score, lives, difficulty):
        """
        Desenha a HUD horizontalmente na parte superior com background preto.
        
        Args:
            window: Surface do pygame
            player: Objeto do jogador
            level: Nível atual
            dodged: Quantidade de desvios realizados
            dodge_target: Alvo de desvios para passar de nível
            score: Pontuação atual
            lives: Vidas restantes
            difficulty: Nome da dificuldade
        """
        # Desenhar background preto da HUD
        pygame.draw.rect(window, C_BLACK, (0, 0, WINDOW_WIDTH, self.hud_height))
        
        # Desenhar borda amarela inferior
        pygame.draw.line(window, C_YELLOW, (0, self.hud_height), (WINDOW_WIDTH, self.hud_height), thickness=2)
        
        # Posições e espaçamento
        y_text = 12  # Posição vertical do texto
        x_start = 15  # Posição inicial horizontal
        spacing = 190  # Espaço entre cada informação
        
        # 1. SCORE (Amarelo)
        score_text = self.font_hud.render(f"SCORE: {score}", True, C_YELLOW)
        window.blit(score_text, (x_start, y_text))
        
        # 2. VIDAS (Branco)
        x_start += spacing
        lives_text = self.font_hud.render(f"VIDAS: {lives}", True, C_WHITE)
        window.blit(lives_text, (x_start, y_text))
        
        # 3. NIVEL (Cor dinâmica baseada na dificuldade)
        x_start += spacing
        nivel_color = self._get_difficulty_color(difficulty)
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
        
        # Barra de progresso (lado direito)
        self._draw_progress_bar(window, WINDOW_WIDTH - 210, 12, 200, 26, dodged / dodge_target if dodge_target > 0 else 0)
    
    def _draw_progress_bar(self, window, x, y, width, height, progress):
        """
        Desenha uma barra de progresso.
        
        Args:
            window: Surface do pygame
            x, y: Posição da barra
            width, height: Dimensões da barra
            progress: Progresso (0.0 a 1.0)
        """
        # Clamp progress entre 0 e 1
        progress = max(0.0, min(1.0, progress))
        
        # Background da barra (cinza escuro)
        pygame.draw.rect(window, C_DARK_GRAY, (x, y, width, height))
        
        # Barra preenchida (amarela)
        filled_width = width * progress
        pygame.draw.rect(window, C_YELLOW, (x, y, filled_width, height))
        
        # Borda branca
        pygame.draw.rect(window, C_WHITE, (x, y, width, height), thickness=2)
        
        # Percentual de progresso
        percentage = int(progress * 100)
        percent_text = self.font_hud_small.render(f"{percentage}%", True, C_WHITE)
        percent_rect = percent_text.get_rect(center=(x + width // 2, y + height // 2))
        window.blit(percent_text, percent_rect)
    
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
        """
        Desenha a tela de game over.
        
        Args:
            window: Surface do pygame
            score: Pontuação final
            level: Nível alcançado
            difficulty: Dificuldade jogada
        """
        # Fundo semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(C_BLACK)
        window.blit(overlay, (0, 0))
        
        # Título
        font_title = pygame.font.SysFont("Lucida Sans Typewriter", 60, bold=True)
        title = font_title.render("GAME OVER", True, C_RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        window.blit(title, title_rect)
        
        # Informações
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
        
        # Instruções
        font_small = pygame.font.SysFont("Lucida Sans Typewriter", 18)
        instr = font_small.render("Pressione R para reiniciar ou ESC para voltar ao menu", True, C_WHITE)
        instr_rect = instr.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        window.blit(instr, instr_rect)
    
    def draw_name_input_screen(self, window, player_name, is_top_score):
        """
        Desenha a tela de entrada de nome para recordes.
        
        Args:
            window: Surface do pygame
            player_name: Nome digitado até agora
            is_top_score: Se é top score
        """
        # Fundo semi-transparente
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
        
        # Campo de entrada
        input_text = font_text.render(player_name + "_", True, C_YELLOW)
        input_rect = input_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        window.blit(input_text, input_rect)
        
        # Instruções
        font_small = pygame.font.SysFont("Lucida Sans Typewriter", 18)
        instr = font_small.render("ENTER para confirmar | ESC para cancelar (máx 8 caracteres)", True, C_WHITE)
        instr_rect = instr.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        window.blit(instr, instr_rect)
    
    def draw_pause_screen(self, window):
        """
        Desenha a tela de pausa.
        
        Args:
            window: Surface do pygame
        """
        # Fundo semi-transparente
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
    
    def draw_level_up_animation(self, window, level, progress):
        """
        Desenha animação de level up.
        
        Args:
            window: Surface do pygame
            level: Novo nível
            progress: Progresso da animação (0.0 a 1.0)
        """
        # Calcular tamanho e posição baseado no progresso
        size = int(30 + progress * 50)
        alpha = int(255 * (1 - progress))
        
        font = pygame.font.SysFont("Lucida Sans Typewriter", size, bold=True)
        text = font.render(f"LEVEL {level}!", True, C_YELLOW)
        
        # Criar surface com alpha
        text_surface = pygame.Surface((text.get_width() + 20, text.get_height() + 20), pygame.SRCALPHA)
        text_surface.set_alpha(alpha)
        text_surface.blit(text, (10, 10))
        
        # Desenhar no centro
        rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        window.blit(text_surface, rect)
    
    def draw_collision_effect(self, window, x, y, progress):
        """
        Desenha efeito visual de colisão.
        
        Args:
            window: Surface do pygame
            x, y: Posição do efeito
            progress: Progresso do efeito (0.0 a 1.0)
        """
        # Círculo que expande
        radius = int(20 + progress * 30)
        alpha = int(255 * (1 - progress))
        
        # Criar surface com alpha
        effect_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(effect_surface, (*C_RED, alpha), (radius, radius), radius, thickness=3)
        
        rect = effect_surface.get_rect(center=(x, y))
        window.blit(effect_surface, rect)
