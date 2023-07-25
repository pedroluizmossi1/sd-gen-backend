import base64
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor

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