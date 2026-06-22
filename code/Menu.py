import pygame
import sys
from code.Const import WINDOW_WIDTH, WINDOW_HEIGHT, C_ORANGE, C_WHITE, C_YELLOW, C_RED, C_GREEN, C_BLUE, MENU_OPTION, DIFFICULTY_NAMES


class Menu:
    def __init__(self, window, sound_manager):
        self.window = window
        self.sound_manager = sound_manager

        # Tenta carregar fundo do menu, se não existir usa fundo preto
        try:
            self.surf = pygame.image.load('./asset/MenuBg.png').convert_alpha()
        except Exception:
            self.surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.surf.fill((0, 0, 0))

        self.rect = self.surf.get_rect(left=0, top=0)
        self.font_title = pygame.font.SysFont("Lucida Sans Typewriter", 60, bold=True)
        self.font_menu = pygame.font.SysFont("Lucida Sans Typewriter", 28)
        self.font_small = pygame.font.SysFont("Lucida Sans Typewriter", 18)

    def run(self):
        """Loop principal do menu. Retorna (acao, dificuldade)."""
        menu_option = 0
        self.sound_manager.start_menu_music()

        while True:
            self.window.blit(self.surf, self.rect)

            # Título
            title = self.font_title.render("ENDURO 2D", True, C_ORANGE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
            self.window.blit(title, title_rect)

            # Opções do menu
            for i, opt in enumerate(MENU_OPTION):
                color = C_YELLOW if i == menu_option else C_WHITE
                text = self.font_menu.render(opt, True, color)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 230 + 50 * i))
                if i == menu_option:
                    arrow = self.font_menu.render(">", True, C_YELLOW)
                    arr_rect = arrow.get_rect(right=text_rect.left - 15, centery=text_rect.centery)
                    self.window.blit(arrow, arr_rect)
                self.window.blit(text, text_rect)

            footer = self.font_small.render("↑↓ Navegar | ENTER Selecionar | ESC Sair", True, C_WHITE)
            footer_rect = footer.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            self.window.blit(footer, footer_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.sound_manager.play_sfx('menu_move')
                        menu_option = (menu_option + 1) % len(MENU_OPTION)

                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.sound_manager.play_sfx('menu_move')
                        menu_option = (menu_option - 1) % len(MENU_OPTION)

                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.sound_manager.play_sfx('menu_select')
                        selected = MENU_OPTION[menu_option]

                        if selected == "JOGAR":
                            diff = self._select_difficulty()
                            if diff:
                                return "JOGAR", diff

                        elif selected == "DIFICULDADE":
                            self._show_difficulty_info()

                        elif selected == "RECORDS":
                            self._show_records()

                        elif selected == "SAIR":
                            pygame.quit()
                            sys.exit()

                    elif event.key == pygame.K_ESCAPE:
                        self.sound_manager.play_sfx('menu_select')
                        return "SAIR", "Normal"

    def _select_difficulty(self):
        """Tela de seleção de dificuldade."""
        option = 0
        while True:
            self.window.blit(self.surf, self.rect)

            title = self.font_menu.render("SELECIONE A DIFICULDADE", True, C_YELLOW)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 120))
            self.window.blit(title, title_rect)

            for i, name in enumerate(DIFFICULTY_NAMES):
                color = C_YELLOW if i == option else C_WHITE
                size = 40 if i == option else 28
                font = pygame.font.SysFont("Lucida Sans Typewriter", size, bold=(i == option))
                text = font.render(name, True, color)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 230 + 60 * i))
                if i == option:
                    arrow = font.render(">", True, C_YELLOW)
                    arr_rect = arrow.get_rect(right=text_rect.left - 15, centery=text_rect.centery)
                    self.window.blit(arrow, arr_rect)
                self.window.blit(text, text_rect)

            footer = self.font_small.render("↑↓ Navegar | ENTER Confirmar | ESC Voltar", True, C_WHITE)
            footer_rect = footer.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            self.window.blit(footer, footer_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.sound_manager.play_sfx('menu_move')
                        option = (option + 1) % len(DIFFICULTY_NAMES)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.sound_manager.play_sfx('menu_move')
                        option = (option - 1) % len(DIFFICULTY_NAMES)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.sound_manager.play_sfx('menu_select')
                        return DIFFICULTY_NAMES[option]
                    elif event.key == pygame.K_ESCAPE:
                        return None

    def _show_difficulty_info(self):
        """Mostra informações sobre cada dificuldade."""
        from code.Const import DIFFICULTY_OPTIONS

        while True:
            self.window.blit(self.surf, self.rect)

            title = self.font_menu.render("DIFICULDADES", True, C_ORANGE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
            self.window.blit(title, title_rect)

            colors = [C_GREEN, C_YELLOW, C_ORANGE, C_RED]
            for i, name in enumerate(DIFFICULTY_NAMES):
                mult = DIFFICULTY_OPTIONS[i]
                txt = self.font_small.render(
                    f"{name}:  Vel {mult['enemy_speed_mult']}x  Spawn {mult['spawn_mult']}x  Pontos {mult['score_mult']}x",
                    True, colors[i])
                txt_rect = txt.get_rect(center=(WINDOW_WIDTH // 2, 130 + 40 * i))
                self.window.blit(txt, txt_rect)

            footer = self.font_small.render("Pressione ESC para voltar", True, C_WHITE)
            footer_rect = footer.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
            self.window.blit(footer, footer_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.sound_manager.play_sfx('menu_select')
                        return

    def _show_records(self):
        """Mostra o TOP 5 records."""
        from code.Database import Database

        db = Database()
        records = db.get_top5()

        while True:
            self.window.blit(self.surf, self.rect)

            title = self.font_menu.render("TOP 5 RECORDS", True, C_YELLOW)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
            self.window.blit(title, title_rect)

            if not records:
                msg = self.font_small.render("Nenhum recorde ainda! Jogue e faça sua pontuação.", True, C_WHITE)
                msg_rect = msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.window.blit(msg, msg_rect)
            else:
                header = self.font_small.render("Pos  Pontos  Nivel  Dificuldade     Data", True, C_YELLOW)
                header_rect = header.get_rect(center=(WINDOW_WIDTH // 2, 110))
                self.window.blit(header, header_rect)

                diff_colors = {"Fácil": C_GREEN, "Normal": C_YELLOW, "Difícil": C_ORANGE, "Extremo": C_RED}
                for i, rec in enumerate(records):
                    color = diff_colors.get(rec.get('difficulty', 'Normal'), C_WHITE)
                    line = f"{i+1:2d}   {rec.get('score', 0):<<5d}  {rec.get('level', 1):2d}     {rec.get('difficulty', '-'):<<12s} {rec.get('date', '')}"
                    txt = self.font_small.render(line, True, color)
                    txt_rect = txt.get_rect(center=(WINDOW_WIDTH // 2, 150 + 30 * i))
                    self.window.blit(txt, txt_rect)

            footer = self.font_small.render("ESC para voltar", True, C_WHITE)
            footer_rect = footer.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
            self.window.blit(footer, footer_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.sound_manager.play_sfx('menu_select')
                        return