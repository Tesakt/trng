from PIL import Image
import os
import struct

def resize_image(image_path, target_size=(1024, 1024)):
    """
    Resize the image to the target size while keeping the center of the image.
    """
    image = Image.open(image_path)
    width, height = image.size
    left = (width - target_size[0]) / 2
    top = (height - target_size[1]) / 2
    right = (width + target_size[0]) / 2
    bottom = (height + target_size[1]) / 2
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

def dithering(image):
    """
    Apply error diffusion dithering to the image.
    """
    pixels = image.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            oldpixel = pixels[x, y][0]  # Wybierz kanał jasności (luminancji) dla piksela
            newpixel = 255 if oldpixel >= 128 else 0
            pixels[x, y] = (newpixel, newpixel, newpixel)  # Ustaw nową wartość dla wszystkich kanałów
            quant_error = oldpixel - newpixel
            if x + 1 < width:
                pixels[x + 1, y] = tuple(int(a + quant_error * 7 / 16) for a in pixels[x + 1, y])
            if x - 1 >= 0 and y + 1 < height:
                pixels[x - 1, y + 1] = tuple(int(a + quant_error * 3 / 16) for a in pixels[x - 1, y + 1])
            if y + 1 < height:
                pixels[x, y + 1] = tuple(int(a + quant_error * 5 / 16) for a in pixels[x, y + 1])
            if x + 1 < width and y + 1 < height:
                pixels[x + 1, y + 1] = tuple(int(a + quant_error * 1 / 16) for a in pixels[x + 1, y + 1])
    return image

def arnold_cat_map(image, iterations=7):
    """
    Apply Arnold cat map to the image.
    """
    width, height = image.size
    N = width  # Możemy użyć szerokości obrazu jako N, ponieważ zakładamy, że obraz jest kwadratowy
    p, q = 1, 1  # Parametry mapy kota Arnolda

    for _ in range(iterations):
        new_image = Image.new("L", (width, height))  # Tworzymy nowy obraz w skali szarości

        for x in range(width):
            for y in range(height):
                nx = (x + p * y) % N
                ny = (q * x + (p * q + 1) * y) % N
                new_image.putpixel((nx, ny), image.getpixel((x, y)))

        image = new_image

    return image

def encrypt_image_blocks(image):
    """
    Encrypt the blocks of the encrypted binary image.
    """
    width, height = image.size
    encrypted_blocks = []

    for y in range(0, height, 4):
        row = []
        for x in range(0, width, 4):
            black_pixel_count = 0

            for dy in range(4):
                for dx in range(4):
                    pixel = image.getpixel((x + dx, y + dy))
                    if pixel == 0:
                        black_pixel_count += 1

            encrypted_value = 0 if black_pixel_count % 2 == 0 else 1
            row.append(encrypted_value)

        encrypted_blocks.append(row)
    return encrypted_blocks


def zigzag_scan(matrix):
    if not matrix:
        return []

    result = []
    rows, cols = len(matrix), len(matrix[0])
    row, col = 0, 0
    going_down = True

    while row < rows and col < cols:
        result.append(matrix[row][col])
        if going_down:
            if row == rows - 1:
                col += 1
                going_down = False
            elif col == 0:
                row += 1
                going_down = False
            else:
                row += 1
                col -= 1
        else:
            if col == cols - 1:
                row += 1
                going_down = True
            elif row == 0:
                col += 1
                going_down = True
            else:
                row -= 1
                col += 1

    return [result[i:i+128] for i in range(0, len(result), 128)]


def process_image(image_path):
    """
    Process the image: resize and apply error diffusion dithering.
    Return the binary image.
    """
    resized_image = resize_image(image_path)
    dithered_image = dithering(resized_image)
    binary_image = dithered_image.convert('1')
    chaos_image = arnold_cat_map(binary_image)  # Otrzymujemy obiekt typu Image
    encrypted_blocks = encrypt_image_blocks(chaos_image)  # Otrzymujemy listę bloków
    combined_sequence = zigzag_scan(encrypted_blocks)  # Przekazujemy listę bloków do funkcji zigzag_scan

    combined_sequence_str = ''.join(str(pixel) for block in combined_sequence for pixel in block)

    return combined_sequence_str

def process_images_in_folder(folder_path):
    """
    Process all images in the specified folder: resize, apply error diffusion dithering,
    and append the result to random_sequence.txt.
    """
    # Pobierz listę plików z rozszerzeniem .jpg z folderu źródłowego
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    
    # Wyczyść zawartość pliku random_sequence.txt, jeśli już istnieje
    if os.path.exists("random_sequence.bin"):
        open("random_sequence.bin", "wb").close()
    
    # Przetwórz każdy obraz z folderu i zapisz wynik do pliku
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        random_sequence = process_image(image_path)
        binary_data = bytes(int(random_sequence[i:i+8], 2) for i in range(0, len(random_sequence), 8))
        with open("random_sequence.bin", "ab") as file:
            file.write(binary_data)


folder_path = "src"  # Ścieżka do folderu z obrazami
process_images_in_folder(folder_path)
print("Random sequence saved to random_sequence.bin")