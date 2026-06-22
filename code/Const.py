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

# ============================================================
# SEÇÃO 6 - BIOMAS / TRECHOS DINÂMICOS
# ============================================================
# Cada bioma define: cor da vegetação, cor do asfalto, cor das bordas,
# cor das faixas, estilo das faixas ('dashed' ou 'solid'), nome do bioma.
# O jogo alterna aleatoriamente entre eles conforme o jogador avança.

BIOMES = [
    {
        'name': 'Floresta',
        'grass_color': (34, 139, 34),       # Verde floresta
        'road_color': (50, 50, 50),          # Asfalto escuro
        'border_color': (255, 255, 0),       # Borda amarela
        'lane_color': (255, 255, 255),       # Faixa branca
        'lane_style': 'dashed',              # Tracejada
    },
    {
        'name': 'Deserto',
        'grass_color': (210, 180, 120),      # Areia
        'road_color': (80, 70, 60),          # Asfalto mais claro (terra)
        'border_color': (255, 255, 255),     # Borda branca
        'lane_color': (255, 255, 0),         # Faixa amarela
        'lane_style': 'solid',               # Contínua
    },
    {
        'name': 'Estrada de Terra',
        'grass_color': (107, 142, 35),       # Verde oliva
        'road_color': (139, 90, 43),         # Terra/marrom
        'border_color': (255, 255, 255),     # Borda branca
        'lane_color': (255, 255, 200),       # Faixa creme
        'lane_style': 'dashed',              # Tracejada
    },
    {
        'name': 'Cidade',
        'grass_color': (80, 80, 80),         # Calçada cinza
        'road_color': (40, 40, 40),          # Asfalto bem escuro
        'border_color': (255, 200, 0),       # Borda amarelo ouro
        'lane_color': (255, 255, 255),       # Faixa branca
        'lane_style': 'solid',               # Contínua
    },
    {
        'name': 'Noturno',
        'grass_color': (20, 50, 20),         # Verde muito escuro
        'road_color': (30, 30, 30),          # Asfalto quase preto
        'border_color': (255, 140, 0),       # Borda laranja
        'lane_color': (255, 255, 0),         # Faixa amarela
        'lane_style': 'dashed',              # Tracejada
    },
    {
        'name': 'Neve',
        'grass_color': (220, 230, 240),      # Branco azulado (neve)
        'road_color': (100, 100, 110),       # Asfalto cinza claro
        'border_color': (200, 200, 200),     # Borda cinza claro
        'lane_color': (255, 255, 255),       # Faixa branca
        'lane_style': 'solid',               # Contínua
    },
    {
        'name': 'Campo',
        'grass_color': (124, 185, 50),       # Verde claro (campo)
        'road_color': (60, 60, 55),          # Asfalto médio
        'border_color': (255, 255, 0),       # Borda amarela
        'lane_color': (255, 255, 255),       # Faixa branca
        'lane_style': 'dashed',              # Tracejada
    },
]

# Intervalo em frames para trocar de bioma (quanto maior, mais tempo no mesmo bioma)
BIOME_CHANGE_INTERVAL = 600  # ~10 segundos a 60 FPS

# ============================================================
# SEÇÃO 7 - DIFICULDADES
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
# SEÇÃO 8 - NÍVEIS
# ============================================================
LEVEL_ENEMY_COUNTS = [5, 10, 15, 20, 25]

# ============================================================
# SEÇÃO 9 - CONFIGURAÇÕES GLOBAIS
# ============================================================
PLAYER_LIVES = 3
POINTS_PER_ENEMY = 10

# ============================================================
# SEÇÃO 10 - MENU
# ============================================================
MENU_OPTION = ("JOGAR", "DIFICULDADE", "RECORDS", "SAIR")

# ============================================================
# SEÇÃO 11 - OBJETOS DE CENÁRIO (LATERAIS)
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
        'fallback_color': (0, 100, 0),
    },
    'person': {
        'files': ['person1.png', 'person2.png', 'person3.png'],
        'width': 25,
        'height': 50,
        'fallback_color': (200, 150, 100),
    },
    'animal': {
        'files': ['animal1.png', 'animal2.png', 'animal3.png'],
        'width': 35,
        'height': 30,
        'fallback_color': (139, 90, 43),
    },
}
