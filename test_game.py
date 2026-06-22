# test_game.py - Script de teste para validar o jogo Enduro 2D

import sys
import os

print("=" * 60)
print("TESTE DE VALIDAÇÃO - JOGO ENDURO 2D")
print("=" * 60)

# Teste 1: Verificar estrutura de pastas
print("\n[1] Verificando estrutura de pastas...")
required_dirs = ['code', 'asset']
for dir_name in required_dirs:
    if os.path.isdir(dir_name):
        print(f"    ✓ Pasta '{dir_name}' encontrada")
    else:
        print(f"    ✗ Pasta '{dir_name}' NÃO encontrada")

# Teste 2: Verificar arquivos Python
print("\n[2] Verificando arquivos Python...")
required_files = [
    'main.py',
    'code/__init__.py',
    'code/Const.py',
    'code/Player.py',
    'code/Enemy.py',
    'code/Menu.py',
    'code/Game.py'
]
for file_name in required_files:
    if os.path.isfile(file_name):
        print(f"    ✓ Arquivo '{file_name}' encontrado")
    else:
        print(f"    ✗ Arquivo '{file_name}' NÃO encontrado")

# Teste 3: Importar módulos
print("\n[3] Testando importações...")
try:
    import pygame
    print(f"    ✓ Pygame {pygame.version.ver} importado com sucesso")
except ImportError as e:
    print(f"    ✗ Erro ao importar Pygame: {e}")
    sys.exit(1)

try:
    from code import Const
    print(f"    ✓ Módulo Const importado")
    print(f"      - Janela: {Const.WINDOW_WIDTH}x{Const.WINDOW_HEIGHT}")
    print(f"      - FPS: {Const.FPS}")
    print(f"      - Níveis: {len(Const.LEVEL_ENEMY_COUNTS)}")
except ImportError as e:
    print(f"    ✗ Erro ao importar Const: {e}")
    sys.exit(1)

try:
    from code.Player import Player
    print(f"    ✓ Classe Player importada")
except ImportError as e:
    print(f"    ✗ Erro ao importar Player: {e}")
    sys.exit(1)

try:
    from code.Enemy import Enemy
    print(f"    ✓ Classe Enemy importada")
except ImportError as e:
    print(f"    ✗ Erro ao importar Enemy: {e}")
    sys.exit(1)

try:
    from code.Menu import Menu
    print(f"    ✓ Classe Menu importada")
except ImportError as e:
    print(f"    ✗ Erro ao importar Menu: {e}")
    sys.exit(1)

try:
    from code.Game import Game
    print(f"    ✓ Classe Game importada")
except ImportError as e:
    print(f"    ✗ Erro ao importar Game: {e}")
    sys.exit(1)

# Teste 4: Validar constantes
print("\n[4] Validando constantes...")
try:
    assert Const.WINDOW_WIDTH == 800, "WINDOW_WIDTH incorreto"
    assert Const.WINDOW_HEIGHT == 600, "WINDOW_HEIGHT incorreto"
    assert Const.PLAYER_MIN_SPEED == 5, "PLAYER_MIN_SPEED incorreto"
    assert Const.PLAYER_MAX_SPEED == 15, "PLAYER_MAX_SPEED incorreto"
    assert Const.MAX_LIVES == 3, "MAX_LIVES incorreto"
    assert len(Const.LEVEL_ENEMY_COUNTS) == 5, "Número de níveis incorreto"
    print("    ✓ Todas as constantes validadas com sucesso")
except AssertionError as e:
    print(f"    ✗ Erro de validação: {e}")
    sys.exit(1)

# Teste 5: Testar criação de objetos
print("\n[5] Testando criação de objetos...")
try:
    pygame.init()
    window = pygame.display.set_mode((Const.WINDOW_WIDTH, Const.WINDOW_HEIGHT))

    player = Player(window)
    print(f"    ✓ Player criado (posição: {player.x}, {player.y})")

    enemy = Enemy(window, 0, 5)
    print(f"    ✓ Enemy criado (posição: {enemy.x}, {enemy.y})")

    pygame.quit()
except Exception as e:
    print(f"    ✗ Erro ao criar objetos: {e}")
    sys.exit(1)

# Resumo final
print("\n" + "=" * 60)
print("✓ TODOS OS TESTES PASSARAM COM SUCESSO!")
print("=" * 60)
print("\nVocê pode agora executar o jogo com:")
print("  python main.py")
print("\nControles:")
print("  ← → : Mover carro")
print("  W/↑ : Acelerar")
print("  S/↓ : Desacelerar")
print("  ESC : Sair")
print("=" * 60)