from flask import Flask, request, jsonify
#import pytesseract
import PyPDF2
from PIL import Image
from flask_cors import CORS
from RelevantYTVidGenerator import generate_yt_insights, generate_yt_titles
import Database

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
		return text(file)
	elif file.endswith('.pdf'):
		return pdf(file)
	else:
		return pic(file)

app = Flask(__name__)
CORS(app)

@app.route('/run_script', methods=['POST'])
def run_script():
    # Assuming the input file is sent as form data
    input_file_wonky = request.files['file']
    input_file = input_file_wonky.stream.read()
    input_email = request.form.get('email')
    print(input_email)
    print(type(input_file))
    #The email and the file are contained inside this!!!!!!!!!!!!!!!!
    # Process the file or data as needed
    ''''
    return jsonify({
        'links': ["https://coolmathgames.com", "https://star trek.com", "https://taylorswift.com","https://google.co.uk","https://ic.ac.uk"],
        'thumbnails': ["https://i.ytimg.com/vi/cPG6nJRJeWQ/default.jpg","https://i.ytimg.com/vi/cPG6nJRJeWQ/default.jpg","https://i.ytimg.com/vi/cPG6nJRJeWQ/default.jpg","https://i.ytimg.com/vi/cPG6nJRJeWQ/default.jpg","https://i.ytimg.com/vi/cPG6nJRJeWQ/default.jpg"],
        'titles': ["TEST2", "ST", "TS", "Goog", "IC"]
    })
    '''
    text = select(input_file)
    print(text)
    urls, thumbnails, titles = generate_yt_titles(text, 5) #generate the relevant urls and thumnails, need to get titles as well
    insights, insight_urls, insight_thumbnails = generate_yt_insights(text) #generate the insights and relevant videos
    Database.add_entries(input_email, insight_urls, insights, insight_thumbnails) #datebot
    
    return jsonify({
        'links': urls, #["https://coolmathgames.com", "https://star trek.com", "https://taylorswift.com","https://google.co.uk","https://ic.ac.uk"],
        'thumbnails': thumbnails,
        'titles': titles
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
