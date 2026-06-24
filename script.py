from PIL import Image
import numpy as np
from pathlib import Path

pasta = Path(r"D:\UNINTER_PROVISORIOS\TrabalhoPygame\asset\picture")

for arquivo in pasta.glob("*.png"):
    if "_fix" in arquivo.stem:
        continue
    img = Image.open(arquivo).convert("RGBA")
    dados = np.array(img)
    # Torna pixels brancos/quase brancos (>240) em transparentes
    mascara = (dados[:,:,0] > 240) & (dados[:,:,1] > 240) & (dados[:,:,2] > 240)
    # Só altera pixels que ainda não são transparentes
    mascara = mascara & (dados[:,:,3] > 0)
    quantidade = int(np.sum(mascara))
    dados[mascara, 3] = 0
    Image.fromarray(dados).save(arquivo, "PNG")
    print(f"✅ {arquivo.name}: {quantidade} pixels brancos removidos")