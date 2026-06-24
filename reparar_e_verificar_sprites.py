from PIL import Image
import numpy as np
from pathlib import Path

pasta = Path(r"D:\UNINTER_PROVISORIOS\TrabalhoPygame\asset\picture")

for arquivo in pasta.glob("*.png"):
    img = Image.open(arquivo).convert("RGBA")
    dados = np.array(img)
    
    # Remove pixels ACIMA de 200 (mais agressivo que 240)
    # Pega também os cinzas claros do anti-aliasing
    mascara = (dados[:,:,0] > 200) & (dados[:,:,1] > 200) & (dados[:,:,2] > 200)
    mascara = mascara & (dados[:,:,3] > 0)
    
    quantidade = int(np.sum(mascara))
    dados[mascara, 3] = 0
    
    Image.fromarray(dados).save(arquivo, "PNG")
    print(f"✅ {arquivo.name}: {quantidade} pixels removidos (limiar 200)")