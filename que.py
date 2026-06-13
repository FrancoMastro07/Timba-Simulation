from PIL import Image
from collections import deque
import os

origenes = ["imagenes/salio", "imagenes/no_salio"]

for origen in origenes:

    destino = origen + "_sin_fondo"
    os.makedirs(destino, exist_ok=True)

    for archivo in os.listdir(origen):

        if not archivo.lower().endswith(".png"):
            continue

        ruta = os.path.join(origen, archivo)

        img = Image.open(ruta).convert("RGBA")
        pixels = img.load()

        width, height = img.size

        cola = deque()

        esquinas = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1)
        ]

        for x, y in esquinas:
            cola.append((x, y))

        while cola:

            x, y = cola.popleft()

            if x < 0 or x >= width or y < 0 or y >= height:
                continue

            r, g, b, a = pixels[x, y]

            if not (r > 240 and g > 240 and b > 240):
                continue

            pixels[x, y] = (255, 255, 255, 0)

            cola.append((x + 1, y))
            cola.append((x - 1, y))
            cola.append((x, y + 1))
            cola.append((x, y - 1))

        img.save(os.path.join(destino, archivo))

print("Listo")