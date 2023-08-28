import json
import random
from config_core import get_config

FACESWAP = """
{
  "25": {
    "inputs": {
      "images": [
        "70",
        0
      ]
    },
    "class_type": "PreviewImage"
  },
  "69": {
    "inputs": {
      "faceswap_model": "inswapper_128.onnx"
    },
    "class_type": "Load Face Swap Model (mtb)"
  },
  "70": {
    "inputs": {
      "aligned": false,
      "only_center_face": false,
      "weight": 0.5,
      "save_tmp_steps": true,
      "image": [
        "80",
        0
      ],
      "model": [
        "71",
        0
      ]
    },
    "class_type": "Restore Face (mtb)"
  },
  "71": {
    "inputs": {
      "model_name": "GFPGANv1.4.pth",
      "upscale": 1
    },
    "class_type": "Load Face Enhance Model (mtb)"
  },
  "80": {
    "inputs": {
      "faces_index": "0",
      "image": [
        "90",
        0
      ],
      "reference": [
        "91",
        0
      ],
      "faceanalysis_model": [
        "81",
        0
      ],
      "faceswap_model": [
        "69",
        0
      ]
    },
    "class_type": "Face Swap (mtb)"
  },
  "81": {
    "inputs": {
      "faceswap_model": "buffalo_l"
    },
    "class_type": "Load Face Analysis Model (mtb)"
  },
  "90": {
    "inputs": {
      "url": ""
    },
    "class_type": "Load Image From Url (mtb)"
  },
  "91": {
    "inputs": {
      "url": ""
    },
    "class_type": "Load Image From Url (mtb)"
  }
}
"""

FACESWAP_NO_UPSCALE = """
{
  "69": {
    "inputs": {
      "faceswap_model": "inswapper_128.onnx"
    },
    "class_type": "Load Face Swap Model (mtb)"
  },
  "75": {
    "inputs": {
      "images": [
        "80",
        0
      ]
    },
    "class_type": "PreviewImage"
  },
  "76": {
    "inputs": {
      "url": ""
    },
    "class_type": "Load Image From Url (mtb)"
  },
  "80": {
    "inputs": {
      "faces_index": "0",
      "image": [
        "93",
        0
      ],
      "reference": [
        "76",
        0
      ],
      "faceanalysis_model": [
        "81",
        0
      ],
      "faceswap_model": [
        "69",
        0
      ]
    },
    "class_type": "Face Swap (mtb)"
  },
  "81": {
    "inputs": {
      "faceswap_model": "buffalo_l"
    },
    "class_type": "Load Face Analysis Model (mtb)"
  },
  "93": {
    "inputs": {
      "url": ""
    },
    "class_type": "Load Image From Url (mtb)"
  }
}
"""

def faceswap_exporter(target_image_id = None,reference_image_id = None, target_image_url = None, reference_image_url = None, upscale = True, face_index = 0):
    fast_api_url = get_config("FASTAPI","fastapi_endpoint_url")
    if upscale:
      faceswap_api = json.loads(FACESWAP)
      if target_image_url:
          faceswap_api["90"]["inputs"]["url"] = target_image_url
      if reference_image_url:
          faceswap_api["91"]["inputs"]["url"] = reference_image_url
      if target_image_id:
          faceswap_api["90"]["inputs"]["url"] = f"{fast_api_url}/user/image/faceswap/?image_id={target_image_id}"
      if reference_image_id:
          faceswap_api["91"]["inputs"]["url"] = f"{fast_api_url}/user/image/faceswap/?image_id={reference_image_id}"
      if face_index:
          faceswap_api["80"]["inputs"]["faces_index"] = face_index
    else:
      faceswap_api = json.loads(FACESWAP_NO_UPSCALE)
      if target_image_url:
          faceswap_api["93"]["inputs"]["url"] = target_image_url
      if reference_image_url:
          faceswap_api["76"]["inputs"]["url"] = reference_image_url
      if target_image_id:
          faceswap_api["93"]["inputs"]["url"] = f"{fast_api_url}/user/image/faceswap/?image_id={target_image_id}"
      if reference_image_id:
          faceswap_api["76"]["inputs"]["url"] = f"{fast_api_url}/user/image/faceswap/?image_id={reference_image_id}"
      if face_index:
          faceswap_api["80"]["inputs"]["faces_index"] = face_index
    return faceswap_api
    