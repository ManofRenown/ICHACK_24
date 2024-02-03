#!/usr/bin/python
import pytesseract
from PIL import Image

# Open the image
image = Image.open('image.png')

# Perform OCR
custom_config = r'--oem 3 --psm 6 -l eng'
text = pytesseract.image_to_string(image, config=custom_config)

print(text)


