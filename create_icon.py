import base64
import struct
import zlib

def create_png(width, height, pixels):
    """Create a minimal PNG file from raw RGBA pixel data."""
    
    def png_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)
    
    # PNG signature
    png = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    png += png_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk (compressed image data)
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # filter byte
        for x in range(width):
            idx = (y * width + x) * 4
            raw_data += bytes(pixels[idx:idx+4])
    
    compressed = zlib.compress(raw_data, 9)
    png += png_chunk(b'IDAT', compressed)
    
    # IEND chunk
    png += png_chunk(b'IEND', b'')
    
    return png

# Create a 512x512 icon with gradient background
width, height = 512, 512
pixels = bytearray(width * height * 4)

# Colors
bg_top = (99, 102, 241)    # #6366F1
bg_bottom = (129, 140, 248) # #818CF8
white = (255, 255, 255)
light_purple = (165, 180, 252)  # #A5B4FC

for y in range(height):
    for x in range(height):
        idx = (y * width + x) * 4
        
        # Calculate gradient
        t = y / height
        r = int(bg_top[0] + (bg_bottom[0] - bg_top[0]) * t)
        g = int(bg_top[1] + (bg_bottom[1] - bg_top[1]) * t)
        b = int(bg_top[2] + (bg_bottom[2] - bg_top[2]) * t)
        
        # Circle mask (centered, radius 256)
        cx, cy = width // 2, height // 2
        dx, dy = x - cx, y - cy
        dist = (dx * dx + dy * dy) ** 0.5
        
        if dist <= 240:
            # Inside circle - white background
            r, g, b = 255, 255, 255
        else:
            # Outside circle - transparent or gradient
            r, g, b = bg_top[0], bg_top[1], bg_top[2]
        
        pixels[idx:idx+4] = [r, g, b, 255]

# Draw book shape (simplified)
book_y_start = 200
book_y_end = 380
book_center_x = width // 2

for y in range(book_y_start, book_y_end):
    for x in range(width):
        idx = (y * width + x) * 4
        dx = x - book_center_x
        
        # Left page
        if -120 <= dx < 0:
            page_y = (y - book_y_start) / (book_y_end - book_y_start)
            curve = int(60 * page_y)
            if -120 + curve <= dx < 0:
                # White page
                pixels[idx:idx+4] = [255, 255, 255, 255]
                # Add text lines
                if y > book_y_start + 60 and y < book_y_end - 40:
                    if (y - book_y_start - 60) % 25 < 6:
                        if dx < -30:
                            pixels[idx:idx+4] = light_purple + (255,)
        
        # Right page
        if 0 <= dx < 120:
            page_y = (y - book_y_start) / (book_y_end - book_y_start)
            curve = int(60 * page_y)
            if 0 <= dx < 120 - curve:
                # White page
                pixels[idx:idx+4] = [255, 255, 255, 255]
                # Add text lines
                if y > book_y_start + 60 and y < book_y_end - 40:
                    if (y - book_y_start - 60) % 25 < 6:
                        if dx > 30:
                            pixels[idx:idx+4] = light_purple + (255,)

# Draw speech bubble with "W"
bubble_x, bubble_y = 340, 120
bubble_r = 50
for y in range(height):
    for x in range(width):
        idx = (y * width + x) * 4
        dx, dy = x - bubble_x, y - bubble_y
        dist = (dx * dx + dy * dy) ** 0.5
        
        if dist <= bubble_r:
            pixels[idx:idx+4] = [255, 255, 255, 255]

# Draw "W" letter
w_font = [
    "  ##   ##  ",
    "  # # # #  ",
    "  #  #  #  ",
    "  #     #  ",
    "  #     #  ",
]
char_w = 11
char_h = 5
char_x = bubble_x - char_w * 3
char_y = bubble_y - 20

for row, line in enumerate(w_font):
    for col, char in enumerate(line):
        px = char_x + col * 6
        py = char_y + row * 8
        if char == '#':
            for dy in range(8):
                for dx in range(6):
                    if 0 <= px + dx < width and 0 <= py + dy < height:
                        idx = ((py + dy) * width + (px + dx)) * 4
                        pixels[idx:idx+4] = [99, 102, 241, 255]  # Purple

# Generate PNG
png_data = create_png(width, height, pixels)

output_path = r'c:\Users\Robert\WorkBuddy\20260427161746\word-learning-app\icon.png'
with open(output_path, 'wb') as f:
    f.write(png_data)

print(f'Icon PNG created at {output_path}!')
