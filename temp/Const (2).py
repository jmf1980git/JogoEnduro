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

# Lista de arquivos de imagem dos carros inimigos (em asset/picture/)
# Adicione quantos modelos quiser - o jogo escolhe aleatoriamente
ENEMY_CAR_FILES = [
    'enemy_car1.png',
    'enemy_car2.png',
]

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

# --- CORES DA ESTRADA (customize aqui!) ---
ROAD_COLOR = (50, 50, 50)          # Cor do asfalto (cinza escuro)
ROAD_BORDER_COLOR = (255, 255, 0)  # Cor das bordas da estrada (amarelo)
ROAD_LANE_COLOR = (255, 255, 255)  # Cor das faixas pontilhadas (branco)
GRASS_COLOR = (34, 139, 34)        # Cor da grama/lateral (verde)

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

# ============================================================
# SEÇÃO 10 - OBJETOS DE CENÁRIO (LATERAIS)
# ============================================================
# Intervalo de frames entre spawns de objetos laterais
SCENERY_SPAWN_INTERVAL = 45

# Multiplicador de velocidade dos objetos laterais em relação ao player
SCENERY_SPEED_MULT = 0.8

# Configuração dos objetos de cenário
# Para cada tipo, liste os arquivos de imagem (em asset/picture/)
# Adicione quantas variações quiser - o jogo escolhe aleatoriamente
SCENERY_OBJECTS = {
    'tree': {
        'files': ['tree1.png', 'tree2.png', 'tree3.png'],
        'width': 40,
        'height': 60,
        'fallback_color': (0, 100, 0),  # Verde escuro
    },
    'person': {
        'files': ['person1.png', 'person2.png', 'person3.png'],
        'width': 25,
        'height': 50,
        'fallback_color': (200, 150, 100),  # Bege
    },
    'animal': {
        'files': ['animal1.png', 'animal2.png', 'animal3.png'],
        'width': 35,
        'height': 30,
        'fallback_color': (139, 90, 43),  # Marrom
    },
}
