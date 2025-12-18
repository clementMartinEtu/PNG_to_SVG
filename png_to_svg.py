from PIL import Image
import math

image = Image.open("image/screenshot.jpg")
image = image.convert("RGB")

px = image.load()
width, height = image.size

# Retrieve all corner points of one hexagon
def hexagon_points(cx, cy, size):
    """
    Compute the 6 corner points of a regular hexagon.

    Args:
        cx (float): X coordinate of the hexagon center.
        cy (float): Y coordinate of the hexagon center.
        size (float): Radius of the hexagon.

    Returns:
        list[tuple[float, float]]: List of 6 (x, y) coordinates of the vertices.

    """
    points = []

    for i in range(6):
        ptx = cx + size * math.cos(math.radians(60 * i - 30))
        pty = cy + size * math.sin(math.radians(60 * i - 30))
        points.append((ptx,pty))

    return points

def sample_color(px, cx, cy, width, height):
    """
    Sample the RGB color of a pixel at the center of a hexagon,
    checking that the coordinates are within image bounds.

    Args:
        px: PIL PixelAccess object.
        cx (float): X coordinate of the hexagon center.
        cy (float): Y coordinate of the hexagon center.
        width (int): Image width.
        height (int): Image height.

    Returns:
        tuple[int, int, int]: RGB color (r, g, b).
        Returns (0, 0, 0) if coordinates are out of bounds.
    """
    if cx >= width or cy >= height:
        return (0, 0, 0)
    return px[int(cx), int(cy)]

def generate_svg(image, hex_size):
    """
    Generate a list of SVG <polygon> elements representing a
    hexagonal tiling of the image.

    Args:
        image: PIL.Image object in RGB mode.
        hex_size (float): Radius of each hexagon.

    Returns:
        list[str]: List of SVG <polygon> strings.
    """
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

    HEX_SIZE = 10

    svg_elements = generate_svg(image, HEX_SIZE)
    #save to svg file
    with open("image/hexagonal.svg", "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
        for element in svg_elements:
            f.write(f"  {element}\n")
        f.write('</svg>\n')
    
    print("SVG file 'image/hexagonal.svg' generated successfully.")