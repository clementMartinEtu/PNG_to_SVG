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

# Sample color at (x, y) checking that it is within bounds
def sample_color(px, cx, cy, width, height):
    if cx >= width or cy >= height:
        return (0, 0, 0)
    return px[int(cx), int(cy)]

def generate_svg(image, hex_size):
    width, height = image.size
    px = image.load()

    dx = math.sqrt(3) * hex_size
    dy = 1.5 * hex_size

    svg_elements = []

    rows = int(height / dy) + 1
    cols = int(width / dx) + 1

    for row in range(rows):
        cy = row * dy
        x_offset = dx / 2 if row % 2 == 1 else 0

        for col in range(cols):
            cx = col * dx + x_offset

            if cx >= width or cy >= height:
                continue

            r, g, b = sample_color(px, cx, cy, width, height)
            color = f"rgb({r},{g},{b})"

            points = hexagon_points(cx, cy, hex_size)
            points_str = " ".join(f"{x},{y}" for x, y in points)

            svg_elements.append(f'<polygon points="{points_str}" fill="{color}" stroke="none"/>')

    return svg_elements

#launch the svg file
if __name__ == '__main__':

    HEX_SIZE = 5

    svg_elements = generate_svg(image, HEX_SIZE)
    #save to svg file
    with open("output_hexagonal.svg", "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
        for element in svg_elements:
            f.write(f"  {element}\n")
        f.write('</svg>\n')

    webbrowser.open("output_hexagonal.svg")