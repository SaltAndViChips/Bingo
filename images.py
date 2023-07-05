import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import warnings
import glob
warnings.filterwarnings("ignore", category=DeprecationWarning)


def text_to_image(text, width, height, font_path, font_size, bg_color, text_color, folder):
    os.makedirs(folder, exist_ok=True)
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Set maximum size of text
    max_text_width = width - 40
    max_text_height = height - 40

    font = ImageFont.truetype(font_path, font_size)

    # Wrap text using textwrap
    wrapped_text = textwrap.wrap(text, width=int((max_text_width) / font_size * 1.5), break_long_words=False,
                                 replace_whitespace=True)

    # Decrease font size until text fits within the image dimensions
    while True:
        text_widths = [draw.textsize(line, font)[0] for line in wrapped_text]
        text_height = font.getsize(wrapped_text[0])[1] * len(wrapped_text)

        if all(width <= max_text_width and height <= max_text_height for width, height in
               zip(text_widths, [text_height] * len(text_widths))):
            break

        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        wrapped_text = textwrap.wrap(text, width=int((max_text_width) / font_size * 1.5), break_long_words=False,
                                     replace_whitespace=True)

    # Draw text onto image
    y = (height - font.getsize(wrapped_text[0])[1] * len(wrapped_text)) // 2 - 10
    for line in wrapped_text:
        x = (width - draw.textsize(line, font)[0]) // 2
        draw.text((x, y), line, font=font, fill=text_color)
        y += font.getsize(line)[1]
        img.save(os.path.join(folder, text + ".png"))

def text_list_to_images(text_list, width, height, font_path, font_size, bg_color, text_color, folder):
    for text in text_list:
        text_to_image(text, width, height, font_path, font_size, bg_color, text_color, folder)

with open('words.txt', 'r') as file:
    text_list = [line.strip() for line in file]
bg_color = (30, 30, 30)
# text_color = "#C819FA"
text_color = "#00FA9A"

if glob.glob(r"images\*.png"):
    print("Cache Detected, Attempting Removal")
    try:
        namecache = []
        for path in glob.glob(r"images\*.png"):
            if "free_space" not in path:
                os.remove(path)
                namecache.append(path.replace("images\\", "").replace(".png", ""))
        print("Files Deleted:\n" + "\n".join(namecache))
    except WindowsError as er:
        print("Could Not Delete:", er)
text_list_to_images(text_list, 800, 800, "arial.ttf", 220, bg_color, text_color, "images")