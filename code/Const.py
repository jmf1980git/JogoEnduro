import pygame

# ============================================================
# SEÇÃO 1 - CONFIGURAÇÕES DA JANELA
# ============================================================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# ============================================================
# SEÇÃO 2 - CORES (RGB)
# ============================================================
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_RED = (220, 20, 60)
C_GREEN = (34, 139, 34)
C_BLUE = (30, 144, 255)
C_YELLOW = (255, 255, 0)
C_ORANGE = (255, 140, 0)
C_GRAY = (100, 100, 100)
C_DARK_GRAY = (50, 50, 50)

# ============================================================
# SEÇÃO 3 - CONFIGURAÇÕES DO PLAYER
# ============================================================
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
PLAYER_SPEED = 8
PLAYER_MIN_SPEED = 5
PLAYER_MAX_SPEED = 15

# ============================================================
# SEÇÃO 4 - CONFIGURAÇÕES DOS INIMIGOS
# ============================================================
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 80
ENEMY_BASE_SPEED = 5
ENEMY_SPAWN_INTERVAL = 90

# ============================================================
# SEÇÃO 5 - CONFIGURAÇÕES DA ESTRADA
# ============================================================
ROAD_LEFT = 150
ROAD_RIGHT = WINDOW_WIDTH - 150
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
NUM_LANES = 3
LANE_WIDTH = ROAD_WIDTH // NUM_LANES

# Posições centrais de cada faixa (para spawn de inimigos)
LANE_CENTERS = [
    ROAD_LEFT + LANE_WIDTH * 0.5,
    ROAD_LEFT + LANE_WIDTH * 1.5,
    ROAD_LEFT + LANE_WIDTH * 2.5,
]

# ============================================================
# SEÇÃO 6 - DIFICULDADES
# ============================================================
DIFFICULTY_NAMES = ["Fácil", "Normal", "Difícil", "Extremo"]

# Índice 0=Fácil, 1=Normal, 2=Difícil, 3=Extremo
DIFFICULTY_OPTIONS = [
    {"enemy_speed_mult": 0.7, "spawn_mult": 1.5, "score_mult": 1.0},
    {"enemy_speed_mult": 1.0, "spawn_mult": 1.0, "score_mult": 1.5},
    {"enemy_speed_mult": 1.4, "spawn_mult": 0.7, "score_mult": 2.0},
    {"enemy_speed_mult": 1.8, "spawn_mult": 0.5, "score_mult": 3.0},
]

# ============================================================
# SEÇÃO 7 - NÍVEIS
# ============================================================
LEVEL_ENEMY_COUNTS = [5, 10, 15, 20, 25]

# ============================================================
# SEÇÃO 8 - CONFIGURAÇÕES GLOBAIS
# ============================================================
PLAYER_LIVES = 3
POINTS_PER_ENEMY = 10

# ============================================================
# SEÇÃO 9 - MENU
# ============================================================
MENU_OPTION = ("JOGAR", "DIFICULDADE", "RECORDS", "SAIR")