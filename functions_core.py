import base64
from PIL import Image
import io
import os
from concurrent.futures import ThreadPoolExecutor
from config_core import get_config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


load_dotenv()
SENDER_EMAIL = os.getenv("GOOGLE_EMAIL_APP")
SENDER_PASSWORD = os.getenv("GOOGLE_EMAIL_APP_PASSWORD")

def base64_image_to_image(base64_image):
    try:
        image_bytes = base64_image.encode('utf-8')
        return base64.decodebytes(image_bytes)
    except Exception as e:
        return {"error": str(e)}
    
def convert_to_webp(image, quality=100):
    try:
        image = Image.open(io.BytesIO(image))
        image_bytes = io.BytesIO()
        image.save(image_bytes, 'webp', quality=quality, method=4)
        return image_bytes.getvalue()
    except Exception as e:
        return {"error": str(e)}

def process_image(image):
    try:
        image = base64_image_to_image(image)
        image = convert_to_webp(image)
        return image
    except Exception as e:
        return {"error": str(e)}
    
def process_images_multithread(images):
    try:
        with ThreadPoolExecutor() as executor:
            return list(executor.map(process_image, images))
    except Exception as e:
        return {"error": str(e)}
    
def process_images_multithread_bytes(images):
    try:
        with ThreadPoolExecutor() as executor:
            return list(executor.map(convert_to_webp, images))
    except Exception as e:
        return {"error": str(e)}

def send_email(receiver_email, subject, body):
    smtp_server, smtp_port = get_config("EMAIL","smtp_server"), get_config("EMAIL","smtp_port")
    print(SENDER_EMAIL, SENDER_PASSWORD)
    try:
        # Set up the email message
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach the email body
        message.attach(MIMEText(body, "plain"))

        # Establish a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Login to your Gmail account
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send the email
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        # Close the connection
        server.quit()

        return True
    except Exception as e:
        return {"error": str(e)}
