import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import markdown2
import os
from dotenv import load_dotenv
load_dotenv()



def extract_video_id(url):
    # Regular expression pattern to match the video ID
    pattern = r'^https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)$'

    # Match the pattern in the URL
    match = re.match(pattern, url)

    # If a match is found, return the video ID
    if match:
        return match.group(1)
    else:
        return None

def generate_html_email(email, url, description):
    # Extract video ID from URL
    video_id = extract_video_id(url)
    
    # If video ID is found, construct embed URL
    if video_id:
        embed_url = f"https://www.youtube.com/embed/{video_id}"
    else:
        return None
    
    # HTML content for the email
    email_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Embedded Video Email</title>
    </head>
    <body>
        <h1>Description:</h1>
        <p>{description}</p>
        
        <!-- Embedded Video -->
        <iframe width="560" height="315" src="{url}" frameborder="0" allowfullscreen></iframe>
    </body>
    </html>
    """

    return email_content

def send_email(email_content, receiver_email):
    
    sender_email =  os.getenv('SENDER_EMAIL')
    receiver_email =  receiver_email
    subject = 'Embedded Video Email'
    password = os.getenv('SENDER_EMAIL_PASSWORD')
    
    # Create MIME message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach HTML content
    message.attach(MIMEText(email_content, 'html'))

    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully")

def embed_image_html(image_url, alt_text="Embedded Image", max_width="80%"):
    """
    Generate HTML code for embedding a responsive image.

    Args:
        image_url (str): The URL of the image.
        alt_text (str): Alt text for the image (default is "Embedded Image").
        max_width (str): Maximum width of the image (default is "100%").

    Returns:
        str: HTML code for embedding the responsive image.
    """
    html_code = f'<img src="{image_url}" alt="{alt_text}">'
    return html_code

def create_clickable_link_html(url, link_text="Click Here"):
    """
    Generate HTML code for a clickable link.

    Args:
        url (str): The URL for the link.
        link_text (str): The text to display for the link (default is "Click Here").

    Returns:
        str: HTML code for the clickable link.
    """
    html_code = f'<a href="{url}" target="_blank">{link_text}</a>'
    return html_code

"""input is a list of dictionaries containing random insights for a specific user"""
def build_email(insight_infos):
    html_content = markdown2.markdown("## Your Daily insights") #convert markdown to html
    for insight_info in insight_infos:
        html_content += markdown2.markdown(insight_info['notes'])
        html_content += "<br>"
        html_content += create_clickable_link_html(insight_info['url'])
        html_content += "<br>"
        html_content += embed_image_html(insight_info['images'])
    return html_content

sender_email =  "ruthvikkonduru29@gmail.com"
receiver_email =  "ruthvikkonduru29@gmail.com"
subject = 'Embedded Video Email'
password = "dkcd ivkw ngmi xokf"
video_url = 'https://www.youtube.com/watch?v=-6G0w_8xToE'
video_description = 'Check out this amazing video!'

"""html_email = generate_html_email(receiver_email, video_url, video_description)
if html_email:
    send_email(sender_email, receiver_email, subject, password, html_email)
    print("Email sent successfully!")
else:
    print("Failed to extract video ID from URL.")"""

highlight2 = """### Importance of OCR
OCR technology is important for businesses as it allows for the conversion of image files, such as scanned documents, into machine-readable text format. 
This enables the utilization of text editing, searching, and word counting functionalities that are not possible with image files. 
It simplifies the process of managing large volumes of paperwork and facilitates paperless document management, ultimately improving efficiency and productivity in business workflows."""

#print(markdown2.markdown(highlight2))

email_html = """<h2>Your Daily insights YO</h2>
<h4>Significance of OCR for Business Workflows</h4>

<p>Business processes heavily rely on print media such as paper forms, invoices, legal documents, and contracts. OCR facilitates the digitization of this content, which is crucial for efficient data analysis, streamlined operations, automated processes, and improved productivity.</p>
<br><a href="https://www.youtube.com/watch?v=23EtQh3wrGA" target="_blank">Click Here</a><br><img src="https://i.ytimg.com/vi/23EtQh3wrGA/default.jpg" alt="Embedded Image"><h4>OCR Text Recognition Methods</h4>

<p>OCR software employs two primary methods for text recognition: pattern matching and feature extraction. While pattern matching compares and matches character images with stored glyphs, feature extraction breaks down glyphs into distinct features to find the best match among stored glyphs.</p>
<br><a href="https://www.youtube.com/watch?v=or8AcS6y1xg" target="_blank">Click Here</a><br><img src="http://res.cloudinary.com/dvs5wlmar/image/upload/Pasted%20image%2020240107173343.png.png" alt="Embedded Image">"""

#<li><img src="http://res.cloudinary.com/dvs5wlmar/image/upload/Pasted%20image%2020240107173343.png.png" alt="Pasted image 20240107173343.png" /></li>

#send_email(email_html,"ruthvikkonduru29@gmail.com")
