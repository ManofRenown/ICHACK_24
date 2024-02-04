from dotenv import load_dotenv
load_dotenv()
import OpenAIFunctions.openaifunctions as openaifunctions
import YoutubeFunctions.youtubefunctions as youtubefunctions
import EmailSender
import Database
from openai import OpenAI
import os
import json
import time
import re

print(os. getcwd())
"""
input: a string containing notes, how many youtube requests
output: list of requests for yt video list
output: urls for relevant youtube vidoes
Function makes request to open ai api to generate 5 requests
Take this request and get 5 requests somehow
Generate yt vidoes based on these requests.
"""
def generate_yt_titles(note, num_requests):

  #get the open ai client object
  api_key = os.getenv('OPENAI_API_KEY') #the env variable
  client = OpenAI()
  client.api_key = api_key

  open_ai_request = f"""Generate {num_requests} YouTube requests to find relevant YouTube videos to the notes above. 
  Do not give the results using a numbered list, instead just use newline to seperate each request. 
  Do not include any other text apart from the youtube requests"""
  full_open_ai_request = note + "\n\n" + open_ai_request

  assistant_id = openaifunctions.create_ytlink_assistant(client) #create new assistant or find assistant that has already been created
  thread_id = client.beta.threads.create().id; #create new thread for this request

  open_ai_response = openaifunctions.send_message(client,assistant_id,thread_id,full_open_ai_request)

  youtube_requests_list = open_ai_response.split('\n') #split each title request assuming they are on new lines
  youtube_requests_list = [re.sub(r'"', '', request.strip()) for request in youtube_requests_list if request] #remove leading and trailing spaces and remove speech marks

  youtube_urls_list = []
  print("open ai response: \n",open_ai_response)
  """print("list: ")
  for request in youtube_requests_list:
    print(request)
    initial_url = youtubefunctions.generate_url(request)
    print(initial_url)

    #youtube_urls_list.append(initial_url)"""
  
  youtube_url_tuples = youtubefunctions.generate_urls(youtube_requests_list, num_requests) #list of tuples containing video url and thumbnail url
  youtube_urls_list = [t[0] for t in youtube_url_tuples] #get all the youtube urls
  youtube_thumbnails_list = [t[1] for t in youtube_url_tuples] #get all the thumbnail urls
  youtube_titles_list = [t[2] for t in youtube_url_tuples] #get all the titles
  return youtube_urls_list, youtube_thumbnails_list, youtube_titles_list #return both lists
  print("url list: ", youtube_urls_list)

def generate_yt_insights(note):

  #get the open ai client object
  api_key = os.environ.get('OPENAI_API_KEY') #the env variable
  client = OpenAI()
  client.api_key = api_key

  open_ai_request = f"""Identify the most important insights from these notes. 
  Each paragraph should be a self contained insight that I can understand without any other context. 
  The format of each paragraph should be title of the paragraph followed by the paragraph. 
  Format these notes very nicely using markdown."""
  full_open_ai_request = note + "\n\n" + open_ai_request

  assistant_id = openaifunctions.create_insight_assistant(client) #create new assistant or find assistant that has already been created
  thread_id = client.beta.threads.create().id; #create new thread for this request

  open_ai_response = openaifunctions.send_message(client,assistant_id,thread_id,full_open_ai_request)

  # Use regular expression to split the string based on Markdown headings
  insights = re.split('#', open_ai_response.strip())
  insights = ['####' + insight for insight in insights if insight != ''] #format all headings as h4

  youtube_urls_list = []
  youtube_thumbnails_list = []
  final_insights_list = [] #we only include insights that actually can find relevant urls
  for insight in insights:
    youtube_urls, youtube_thumbnails, youtube_titles = generate_yt_titles(insight, 1)
    print("the insight: \n" + insight + "\n")
    #print("youtube urls: ", youtube_urls)
    if len(youtube_urls) > 0: #youtube_urls and thumbnails will have the same length
      if len(youtube_urls[0]) > 0: #ensure it actually returns youtube url
        youtube_urls_list.append(youtube_urls[0]) #first element of tuple is url link
        youtube_thumbnails_list.append(youtube_thumbnails[0]) #second element of tuple is the thumbnail link
        final_insights_list.append(insight)

    
    print("the url: ", youtube_urls[0])

  return (final_insights_list, youtube_urls_list, youtube_thumbnails_list)


#####  All this stuff is for debugging functions


notes = """Optical Character Recognition (OCR) is the process that converts an image of text into a machine-readable text format. For example, if you scan a form or a receipt, your computer saves the scan as an image file. You cannot use a text editor to edit, search, or count the words in the image file. However, you can use OCR to convert the image into a text document with its contents stored as text data.
Why is OCR important?

Most business workflows involve receiving information from print media. Paper forms, invoices, scanned legal documents, and printed contracts are all part of business processes. These large volumes of paperwork take a lot of time and space to store and manage. Though paperless document management is the way to go, scanning the document into an image creates challenges. The process requires manual intervention and can be tedious and slow.

Moreover, digitizing this document content creates image files with the text hidden within it. Text in images cannot be processed by word processing software in the same way as text documents. OCR technology solves the problem by converting text images into text data that can be analyzed by other business software. You can then use the data to conduct analytics, streamline operations, automate processes, and improve productivity.
How does OCR work?

The OCR engine or OCR software works by using the following steps:

Image acquisition

A scanner reads documents and converts them to binary data. The OCR software analyzes the scanned image and classifies the light areas as background and the dark areas as text.

Preprocessing

The OCR software first cleans the image and removes errors to prepare it for reading. These are some of its cleaning techniques:

Deskewing or tilting the scanned document slightly to fix alignment issues during the scan.
Despeckling or removing any digital image spots or smoothing the edges of text images.
Cleaning up boxes and lines in the image.
Script recognition for multi-language OCR technology
Text recognition

The two main types of OCR algorithms or software processes that an OCR software uses for text recognition are called pattern matching and feature extraction.

Pattern matching

Pattern matching works by isolating a character image, called a glyph, and comparing it with a similarly stored glyph. Pattern recognition works only if the stored glyph has a similar font and scale to the input glyph. This method works well with scanned images of documents that have been typed in a known font.

Feature extraction

Feature extraction breaks down or decomposes the glyphs into features such as lines, closed loops, line direction, and line intersections. It then uses these features to find the best match or the nearest neighbor among its various stored glyphs.

Postprocessing

After analysis, the system converts the extracted text data into a computerized file. Some OCR systems can create annotated PDF files that include both the before and after versions of the scanned document."""

highlight = """Chinese Youth Slang: "Rùn"
Chinese youths have adopted the slang term "rùn," meaning to flee, as a way to express their desire to escape various pressures, including parental expectations and the challenges of urban life. Over time, it has evolved to signify emigrating from China altogether, with an increasing number of individuals seeking legal migration to Europe or America. Some even take bold routes, like traversing the dangerous Darien Gap to reach Mexico and the United States, contributing to the migrant surge at the southern U.S. border.
"""

highlight2 = """### Importance of OCR
OCR technology is important for businesses as it allows for the conversion of image files, such as scanned documents, into machine-readable text format. This enables the utilization of text editing, searching, and word counting functionalities that are not possible with image files. It simplifies the process of managing large volumes of paperwork and facilitates paperless document management, ultimately improving efficiency and productivity in business workflows."""

"""url, thumbnail, title = generate_yt_titles(notes, 5)
print("final url: ", url)
print("final thumbail: ", thumbnail)
print("final title: ", title)"""

'''
insights, youtube_url_list, youtube_thumbnail_list = generate_yt_insights(notes)



print("final insights: \n")
print(insights)
print("num insights: ", len(insights))
print("\n\nfinal urls: ")
print(youtube_url_list)
print("\n\nthumbnails urls: ")
print(youtube_thumbnail_list)

Database.add_entries("ruthvikkonduru29@gmail.com", youtube_url_list, insights, youtube_thumbnail_list)
insight_infos = Database.get_random_entries("ruthvikkonduru29@gmail.com",2)

print("insight infos: ")
print(insight_infos)

email_html = EmailSender.build_email(insight_infos)

print(email_html)

EmailSender.send_email(email_html, "ruthvikkonduru29@gmail.com")

'''



