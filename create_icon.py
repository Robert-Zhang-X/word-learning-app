from PIL import Image, ImageDraw, ImageFilter
import math

def create_icon():
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    purple1 = (99, 102, 241)    # #6366F1
    purple2 = (124, 58, 237)    # #7C3AED
    purple3 = (139, 92, 246)    # #8B5CF6
    white = (255, 255, 255)
    light_purple = (199, 210, 254)  # #C7D2FE
    light_blue = (240, 244, 255)    # #F0F4FF
    
    corner_radius = 90
    
    # Draw rounded rectangle background
    for y in range(size):
        for x in range(size):
            # Check if inside rounded rect
            dx = min(x, size - 1 - x)
            dy = min(y, size - 1 - y)
            
            # Check corner
            if dx < corner_radius and dy < corner_radius:
                cx, cy = corner_radius, corner_radius
                dist = math.sqrt((dx - cx)**2 + (dy - cy)**2)
                if dist > corner_radius:
                    continue
            
            # Gradient calculation
            t = y / size
            r_c = int(purple1[0] + (purple3[0] - purple1[0]) * t)
            g_c = int(purple1[1] + (purple3[1] - purple1[1]) * t)
            b_c = int(purple1[2] + (purple3[2] - purple1[2]) * t)
            img.putpixel((x, y), (r_c, g_c, b_c, 255))
    
    # Draw decorative circles
    for cx, cy, radius, alpha in [(100, 100, 60, 25), (420, 420, 80, 20), (400, 120, 30, 38)]:
        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                if dx*dx + dy*dy <= radius*radius:
                    px, py = cx + dx, cy + dy
                    if 0 <= px < size and 0 <= py < size:
                        p = img.getpixel((px, py))
                        if p[3] > 0:  # Only draw on background
                            img.putpixel((px, py), (255, 255, 255, alpha))
    
    # Draw book shadow
    shadow_y = 380
    for dy in range(15):
        for dx in range(-130, 131):
            alpha = int(40 * (1 - dy/15))
            sy = shadow_y + dy
            sx = size//2 + dx
            if 0 <= sx < size and 0 <= sy < size:
                p = img.getpixel((sx, sy))
                if p[3] > 0:
                    # Blend shadow
                    factor = alpha / 255
                    new_r = int(p[0] * (1 - factor))
                    new_g = int(p[1] * (1 - factor))
                    new_b = int(p[2] * (1 - factor))
                    img.putpixel((sx, sy), (new_r, new_g, new_b, p[3]))
    
    # Draw open book
    book_y = 180
    book_h = 120
    
    # Left page
    for y in range(book_h):
        for x in range(120):
            px = size//2 - 120 + x
            py = book_y + y
            
            # Calculate curve offset
            t = y / book_h
            curve = int(60 * t)
            
            if x >= curve and 0 <= px < size and 0 <= py < size:
                p = img.getpixel((px, py))
                if p[3] > 0:
                    # Inside page area
                    img.putpixel((px, py), white)
                    
                    # Add text lines
                    line_y = y - 40
                    if 20 <= line_y <= 80 and (line_y - 20) % 20 < 6 and x < 70:
                        img.putpixel((px, py), light_purple)
    
    # Right page
    for y in range(book_h):
        for x in range(120):
            px = size//2 + x
            py = book_y + y
            
            t = y / book_h
            curve = int(60 * t)
            
            if x < 120 - curve and 0 <= px < size and 0 <= py < size:
                p = img.getpixel((px, py))
                if p[3] > 0:
                    img.putpixel((px, py), white)
                    
                    line_y = y - 40
                    if 20 <= line_y <= 80 and (line_y - 20) % 20 < 6 and x > 50:
                        img.putpixel((px, py), light_purple)
    
    # Spine
    for y in range(book_h):
        for x in range(8):
            px = size//2 - 4 + x
            py = book_y - 30 + y
            if 0 <= px < size and 0 <= py < size:
                p = img.getpixel((px, py))
                if p[3] > 0:
                    img.putpixel((px, py), light_blue)
    
    # Draw speech bubble with W
    bubble_x, bubble_y = 350, 130
    bubble_r = 55
    
    for dy in range(-bubble_r, bubble_r+1):
        for dx in range(-bubble_r, bubble_r+1):
            if dx*dx + dy*dy <= bubble_r*bubble_r:
                px, py = bubble_x + dx, bubble_y + dy
                if 0 <= px < size and 0 <= py < size:
                    p = img.getpixel((px, py))
                    if p[3] > 0:
                        img.putpixel((px, py), white)
    
    # Draw W letter using lines
    w_color = purple1
    # W shape points (relative to bubble center)
    w_segments = [
        # Left line
        (bubble_x - 20, bubble_y - 15, bubble_x - 12, bubble_y + 20),
        # Right line
        (bubble_x + 20, bubble_y - 15, bubble_x + 12, bubble_y + 20),
        # Center V
        (bubble_x - 12, bubble_y + 20, bubble_x, bubble_y - 5),
        (bubble_x + 12, bubble_y + 20, bubble_x, bubble_y - 5),
    ]
    
    for x1, y1, x2, y2 in w_segments:
        # Draw thick line
        for t in range(101):
            tx = int(x1 + (x2 - x1) * t / 100)
            ty = int(y1 + (y2 - y1) * t / 100)
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    px, py = tx + dx, ty + dy
                    if 0 <= px < size and 0 <= py < size:
                        p = img.getpixel((px, py))
                        if p[3] > 0:
                            img.putpixel((px, py), w_color)
    
    # Draw floating letters
    letters = [('A', 140, 175), ('B', 175, 135), ('C', 410, 275)]
    for letter, lx, ly in letters:
        for dy in range(-12, 13):
            for dx in range(-8, 9):
                px, py = lx + dx, ly + dy
                if 0 <= px < size and 0 <= py < size:
                    if abs(dx) + abs(dy) < 12:
                        p = img.getpixel((px, py))
                        if p[3] > 0:
                            img.putpixel((px, py), (255, 255, 255, 220))
    
    # Add subtle gradient overlay at edges
    for y in range(size):
        for x in range(size):
            p = img.getpixel((x, y))
            if p[3] > 0:
                cx, cy = x - size//2, y - size//2
                dist = math.sqrt(cx*cx + cy*cy) / (size//2)
                if dist > 0.7:
                    darken = int(15 * (dist - 0.7) / 0.3)
                    new_r = max(0, p[0] - darken)
                    new_g = max(0, p[1] - darken)
                    new_b = max(0, p[2] - darken)
                    img.putpixel((x, y), (new_r, new_g, new_b, p[3]))
    
    return img

# Create and save
img = create_icon()
output_path = r'c:\Users\Robert\WorkBuddy\20260427161746\word-learning-app\icon.png'
img.save(output_path, 'PNG')
print(f'Icon saved to {output_path}')
