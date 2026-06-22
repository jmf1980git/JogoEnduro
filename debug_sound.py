import os
import pygame

# Inicializar pygame e mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

print("=" * 50)
print("VERIFICANDO ARQUIVOS DE SOM")
print("=" * 50)

sound_path = './asset/sound/'
print(f"Pasta de sons: {os.path.abspath(sound_path)}")
print()

# Verificar se a pasta existe
if os.path.exists(sound_path):
    print("✅ Pasta ./asset/sound/ EXISTE")
    print()
    
    # Listar arquivos na pasta
    files = os.listdir(sound_path)
    print(f"Arquivos encontrados ({len(files)}):")
    for f in files:
        fpath = os.path.join(sound_path, f)
        size = os.path.getsize(fpath)
        print(f"   - {f} ({size} bytes)")
    print()
    
    # Verificar especificamente o menu_music
    music_path_ogg = os.path.join(sound_path, 'menu_music.ogg')
    music_path_mp3 = os.path.join(sound_path, 'menu_music.mp3')
    music_path_wav = os.path.join(sound_path, 'menu_music.wav')
    
    if os.path.exists(music_path_ogg):
        print("✅ menu_music.ogg ENCONTRADO")
        try:
            pygame.mixer.music.load(music_path_ogg)
            print("✅ menu_music.ogg CARREGADO com sucesso!")
            pygame.mixer.music.play(-1)
            pygame.time.wait(500)
            if pygame.mixer.music.get_busy():
                print("✅ menu_music.ogg TOCANDO! (ouvirá por 2 segundos...)")
                pygame.time.wait(2000)
                pygame.mixer.music.stop()
            else:
                print("❌ menu_music.ogg carregou mas não está tocando")
        except Exception as e:
            print(f"❌ Erro ao carregar menu_music.ogg: {e}")
    elif os.path.exists(music_path_mp3):
        print("✅ menu_music.mp3 ENCONTRADO (mas SoundManager procura .ogg)")
        print("💡 Dica: renomeie para menu_music.ogg OU mude o código para .mp3")
    elif os.path.exists(music_path_wav):
        print("✅ menu_music.wav ENCONTRADO (mas SoundManager procura .ogg)")
    else:
        print("❌ NENHUM arquivo de música encontrado!")
        print("   Precisa de: menu_music.ogg")
        print("   Baixe em: https://pixabay.com/music/")
else:
    print("❌ Pasta ./asset/sound/ NÃO EXISTE!")
    print("   Crie a pasta: mkdir -p asset/sound")
    print()

# Verificar efeitos sonoros
print("-" * 50)
print("VERIFICANDO EFEITOS SONOROS")
print("-" * 50)

sfx_files = [
    'menu_move.wav', 'menu_select.wav', 'engine.wav',
    'dodge.wav', 'crash.wav', 'level_up.wav',
    'game_over.wav', 'victory.wav'
]

for sfx in sfx_files:
    sfx_path = os.path.join(sound_path, sfx)
    if os.path.exists(sfx_path):
        try:
            s = pygame.mixer.Sound(sfx_path)
            print(f"✅ {sfx} - OK ({os.path.getsize(sfx_path)} bytes)")
        except Exception as e:
            print(f"❌ {sfx} - existe mas não carrega: {e}")
    else:
        print(f"❌ {sfx} - NÃO ENCONTRADO")

print()
print("=" * 50)
print("DICA: Se o menu_music.ogg não existe mas você tem um MP3,")
print("baixe ele como menu_music.ogg ou renomeie.")
print("Sites gratuitos: https://pixabay.com/music/")
print("=" * 50)

pygame.quit()