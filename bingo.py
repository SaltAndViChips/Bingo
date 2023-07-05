import os
import random
from PIL import Image, ImageDraw, ImageFont

# Define the size of the card and the size of each cell
card_width = 1000
card_height = 900
cell_size = (133, 133)

# Create a transparent image with the same size as the card
card_image = Image.new('RGBA', (card_width, card_height), (0, 0, 0, 0))

# Create a drawing context for the card image
draw = ImageDraw.Draw(card_image)

# Load the image files for the free space cell
free_space_image = Image.open('images/free_space.png')

# Randomly select the image files for each cell on the grid
cell_image_files = os.listdir('images')
cell_image_files.remove('free_space.png')
random.shuffle(cell_image_files)
cell_image_files.insert(12, 'free_space.png')

# Load the image files for each cell on the grid
cell_images = []
for file_name in cell_image_files:
    cell_images.append(Image.open(os.path.join('images', file_name)))

# Paste the cell images onto the card with transparent padding
for i in range(5):
    for j in range(5):
        x = j*(cell_size[0]+20) + 20  # Add 20 pixels of padding
        y = (i+1)*(cell_size[1]+20)  # Add 20 pixels of padding and offset the cells downward
        cell_image = cell_images[i*5+j]
        cell_image = cell_image.resize(cell_size, Image.ANTIALIAS)
        card_image.paste(cell_image, (x, y))


# Draw the title text on the card
title_font = ImageFont.truetype('Lato-Bold.ttf', 96)
title_text = 'B      I      N    G    O'
title_text_size = title_font.getsize(title_text)
title_x = int((title_text_size[0])/15)
title_y = 20  # Offset the title downward by 20 pixels to avoid overlapping with the cells
draw.text((title_x, title_y), title_text, fill='#00fa9a', font=title_font)


# Calculate cell size
num_cells_per_row = 5
padding = 10
total_width = 1000
cell_size = int((total_width - (num_cells_per_row + 1) * padding) / num_cells_per_row)

# # Draw the B I N G O letters over each column
# letter_font = ImageFont.truetype('arial.ttf', 32)
# for i, letter in enumerate('BINGO'):
#     letter_size = letter_font.getsize(letter)
#     cell_center_x = cell_size * i + cell_size // 2 + padding * (i + 1)
#     letter_x = cell_center_x - letter_size[0] // 2
#     letter_y = int(cell_size / 2 - letter_size[1] / 2)
#     draw.text((letter_x, letter_y), letter, fill='#00fa9a', font=letter_font)

card_image.save('bingo_card.png')
