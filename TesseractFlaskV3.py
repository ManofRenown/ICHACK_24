from flask import Flask, request, jsonify
#import pytesseract
import PyPDF2
from PIL import Image
from flask_cors import CORS

#Functions for reading the different file types to txt
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

#Finds the file type and runs the appropriate function
def select(file):
	if file.endswith('.txt') or file.endswith('.md') or file.endswith('.html'):
		text(file)
	elif file.endswith('.pdf'):
		pdf(file)
	else:
		pic(file)

app = Flask(__name__)
CORS(app)

@app.route('/run_script', methods=['POST'])
def run_script():
    # Assuming the input file is sent as form data
    input_file = request.files['file']
    # Process the file or data as needed
    ##text = select(input_file)
    #return jsonify({'text': "this is hard coded text"})
    return jsonify({
        'links': ["https://coolmathgames.com", "https://star trek.com", "https://taylorswift.com","https://google.co.uk","https://ic.ac.uk"],
        'thumbnails': ["https://i.ytimg.com/vi/cPG6nJRJeWQ/default.jpg","https://i.ytimg.com/vi/cPG6nJRJeWQ/default.jpg","https://i.ytimg.com/vi/cPG6nJRJeWQ/default.jpg","https://i.ytimg.com/vi/cPG6nJRJeWQ/default.jpg","https://i.ytimg.com/vi/cPG6nJRJeWQ/default.jpg"],
        'titles': ["CMG", "ST", "TS", "Goog", "IC"]
    })
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
