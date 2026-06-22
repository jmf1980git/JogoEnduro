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
PLAYER_WIDTH = 75
PLAYER_HEIGHT = 120
PLAYER_SPEED = 8
PLAYER_MIN_SPEED = 5
PLAYER_MAX_SPEED = 18

# ============================================================
# SEÇÃO 4 - CONFIGURAÇÕES DOS INIMIGOS
# ============================================================
ENEMY_WIDTH = 75
ENEMY_HEIGHT = 120
ENEMY_BASE_SPEED = 6
ENEMY_SPAWN_INTERVAL = 50  # Spawn mais frequente (era 90)

# Lista de arquivos de imagem dos carros inimigos (em asset/picture/)
# Adicione quantos modelos quiser - o jogo escolhe aleatoriamente
ENEMY_CAR_FILES = [
    'enemy_car1.png',
    'enemy_car2.png',
]

# ============================================================
# SEÇÃO 5 - CONFIGURAÇÕES DA ESTRADA
# ============================================================
ROAD_LEFT = 120
ROAD_RIGHT = WINDOW_WIDTH - 120
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
NUM_LANES = 4  # Agora com 4 faixas (era 3)
LANE_WIDTH = ROAD_WIDTH // NUM_LANES

# Posições centrais de cada faixa (para spawn de inimigos)
LANE_CENTERS = [
    ROAD_LEFT + LANE_WIDTH * (i + 0.5) for i in range(NUM_LANES)
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
        'grass_color': (34, 139, 34),
        'road_color': (50, 50, 50),
        'border_color': (255, 255, 0),
        'lane_color': (255, 255, 255),
        'lane_style': 'dashed',
    },
    {
        'name': 'Deserto',
        'grass_color': (210, 180, 120),
        'road_color': (80, 70, 60),
        'border_color': (255, 255, 255),
        'lane_color': (255, 255, 0),
        'lane_style': 'solid',
    },
    {
        'name': 'Estrada de Terra',
        'grass_color': (107, 142, 35),
        'road_color': (139, 90, 43),
        'border_color': (255, 255, 255),
        'lane_color': (255, 255, 200),
        'lane_style': 'dashed',
    },
    {
        'name': 'Cidade',
        'grass_color': (80, 80, 80),
        'road_color': (40, 40, 40),
        'border_color': (255, 200, 0),
        'lane_color': (255, 255, 255),
        'lane_style': 'solid',
    },
    {
        'name': 'Noturno',
        'grass_color': (20, 50, 20),
        'road_color': (30, 30, 30),
        'border_color': (255, 140, 0),
        'lane_color': (255, 255, 0),
        'lane_style': 'dashed',
    },
    {
        'name': 'Neve',
        'grass_color': (220, 230, 240),
        'road_color': (100, 100, 110),
        'border_color': (200, 200, 200),
        'lane_color': (255, 255, 255),
        'lane_style': 'solid',
    },
    {
        'name': 'Campo',
        'grass_color': (124, 185, 50),
        'road_color': (60, 60, 55),
        'border_color': (255, 255, 0),
        'lane_color': (255, 255, 255),
        'lane_style': 'dashed',
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
    {"enemy_speed_mult": 0.8, "spawn_mult": 1.3, "score_mult": 1.0},
    {"enemy_speed_mult": 1.2, "spawn_mult": 0.8, "score_mult": 1.5},
    {"enemy_speed_mult": 1.6, "spawn_mult": 0.5, "score_mult": 2.5},
    {"enemy_speed_mult": 2.0, "spawn_mult": 0.3, "score_mult": 4.0},
]

# ============================================================
# SEÇÃO 8 - NÍVEIS E PROGRESSÃO (INFINITO)
# ============================================================
# Quantidade BASE de desvios para passar a primeira fase
LEVEL_BASE_DODGES = 8

# Incremento de desvios necessários por fase (a cada nível precisa desviar mais)
LEVEL_DODGE_INCREMENT = 4

# Aumento de velocidade dos inimigos por nível (somado a cada fase)
LEVEL_SPEED_INCREMENT = 0.8

# Velocidade máxima dos inimigos (teto para não ficar impossível)
ENEMY_MAX_SPEED = 20

# Redução do intervalo de spawn por nível (em frames)
LEVEL_SPAWN_REDUCTION = 3

# Mínimo de intervalo de spawn (para não ficar impossível)
MIN_SPAWN_INTERVAL = 12

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
SCENERY_SPAWN_INTERVAL = 40

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
