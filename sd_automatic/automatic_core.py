import requests
from config_core import get_config
import mongo.models.image_model as image_model

automatic_host = get_config("AUTOMATIC1111", "automatic_host")
automatic_port = get_config("AUTOMATIC1111", "automatic_port")

automatic_url = f"{automatic_host}:{automatic_port}"

def create_user_image_txt2img(image: image_model.Image.Txt2Img):
    try:
        r = requests.post(f"{automatic_url}/sdapi/v1/txt2img", json=image.dict())
        return r.json()
    except Exception as e:
        return {"error": str(e)}