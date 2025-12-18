from PIL import Image
import math
import webbrowser

image = Image.open("image/screenshot.jpg")
image = image.convert("RGB")

px = image.load()
width, height = image.size

# Retrieve all corner points of one hexagon
def hexagon_points(cx, cy, size):
    points = []

    for i in range(6):
        ptx = cx + size * math.cos(math.radians(60 * i - 30))
        pty = cy + size * math.sin(math.radians(60 * i - 30))
        points.append((ptx,pty))

    return points