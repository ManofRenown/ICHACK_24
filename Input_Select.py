#!/usr/bin/python
import pytesseract
import PyPDF2
from PIL import Image

def select(file):
	if file.endswith('.txt') or file.endswith('.md'):
		text(file)
	elif file.endswith('.pdf'):
		pdf(file)
	else:
		pic(file)

# Open the image
def pic(image_file):
	try:
		image = Image.open(image_file)
	except Exception as e:
		print("error opening file: ", e)
	# Perform OCR
	custom_config = r'--oem 3 --psm 6 -l eng'
	text = pytesseract.image_to_string(image, config=custom_config)
	print("image of printed text")
	print(text)
	return text

def text(text_file):
    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as f:
        reader = PyPDF2.PdfFileReader(f)
        num_pages = reader.numPages
        for page_num in range(num_pages):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text