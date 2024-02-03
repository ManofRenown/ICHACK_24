import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

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
        <iframe width="560" height="315" src="{embed_url}" frameborder="0" allowfullscreen></iframe>
    </body>
    </html>
    """

    return email_content

def send_email(sender_email, receiver_email, subject, password, email_content):
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

sender_email = 'ichackgroup26@gmail.com'
receiver_email = 'sidultimate@outlook.com'
subject = 'Embedded Video Email'
password = 'ichackiscool'
video_url = 'https://www.youtube.com/watch?v=-6G0w_8xToE'
video_description = 'Check out this amazing video!'

html_email = generate_html_email(receiver_email, video_url, video_description)
if html_email:
    send_email(sender_email, receiver_email, subject, password, html_email)
    print("Email sent successfully!")
else:
    print("Failed to extract video ID from URL.")

