"""Module for SDXL prompts exporter."""
import json
import random

SDXL_REFINER = r"""
{
  "4": {
    "inputs": {
      "ckpt_name": "SDXL\\dreamshaperXL10_alpha2Xl10.safetensors"
    },
    "class_type": "CheckpointLoaderSimple"
  },
  "6": {
    "inputs": {
      "text": "dog surfing, beach island, anime style, close view, water splash drops",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "7": {
    "inputs": {
      "text": "(low quality:1.3) (((3D render)))",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "11": {
    "inputs": {
      "ckpt_name": "SDXL\\sd_xl_refiner_1.0.safetensors"
    },
    "class_type": "CheckpointLoaderSimple"
  },
  "12": {
    "inputs": {
      "text": "dog surfing, beach island, anime style, close view, water splash drops",
      "clip": [
        "11",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "13": {
    "inputs": {
      "text": "(low quality:1.3) (((3D render)))",
      "clip": [
        "11",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "17": {
    "inputs": {
      "seed": 1269504746543802,
      "steps": 10,
      "cfg": 7,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "denoise": 1,
      "model": [
        "4",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "21",
        0
      ]
    },
    "class_type": "KSampler"
  },
  "18": {
    "inputs": {
      "samples": [
        "20",
        0
      ],
      "vae": [
        "23",
        0
      ]
    },
    "class_type": "VAEDecode"
  },
  "19": {
    "inputs": {
      "filename_prefix": "sdgen/refiner_output",
      "images": [
        "18",
        0
      ]
    },
    "class_type": "SaveImage"
  },
  "20": {
    "inputs": {
      "seed": 1101064198161382,
      "steps": 5,
      "cfg": 8,
      "sampler_name": "dpmpp_2m",
      "scheduler": "normal",
      "denoise": 0.09999999999999987,
      "model": [
        "11",
        0
      ],
      "positive": [
        "12",
        0
      ],
      "negative": [
        "13",
        0
      ],
      "latent_image": [
        "17",
        0
      ]
    },
    "class_type": "KSampler"
  },
  "21": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage"
  },
  "23": {
    "inputs": {
      "vae_name": "sdxl_vae.safetensors"
    },
    "class_type": "VAELoader"
  }
}
"""

def sdxl_refiner_exporter(positive_prompt, 
                          negative_prompt, 
                          seed, 
                          refiner_seed,
                          refiner_denoise, 
                          width, 
                          height, 
                          batch_size, 
                          model_path, 
                          steps = 10, 
                          cfg = 7,
                          sampler_name = "dpmpp_2m"
                          ):
    """Export SDXL refiner prompt"""

    if seed in (None, 0, "", -1):
        seed = random.randint(0, 99999999999999)
    if refiner_seed in (None, 0, "", -1):
        refiner_seed = random.randint(0, 99999999999999)

    prompt = json.loads(SDXL_REFINER)
    prompt["6"]["inputs"]["text"] = positive_prompt
    prompt["12"]["inputs"]["text"] = positive_prompt
    prompt["7"]["inputs"]["text"] = negative_prompt
    prompt["13"]["inputs"]["text"] = negative_prompt
    prompt["17"]["inputs"]["seed"] = seed
    prompt["17"]["inputs"]["steps"] = steps
    prompt["17"]["inputs"]["cfg"] = cfg
    prompt["17"]["inputs"]["sampler_name"] = sampler_name
    prompt["20"]["inputs"]["seed"] = refiner_seed
    prompt["20"]["inputs"]["denoise"] = refiner_denoise
    prompt["21"]["inputs"]["width"] = width
    prompt["21"]["inputs"]["height"] = height
    prompt["21"]["inputs"]["batch_size"] = batch_size
    prompt["4"]["inputs"]["ckpt_name"] = model_path if model_path else "SDXL\\dreamshaperXL10_alpha2Xl10.safetensors"
    return prompt

SDXL = r"""
{
  "4": {
    "inputs": {
      "ckpt_name": "SDXL\\dreamshaperXL10_alpha2Xl10.safetensors"
    },
    "class_type": "CheckpointLoaderSimple"
  },
  "6": {
    "inputs": {
      "text": "dog surfing, beach island, anime style, close view, water splash drops",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "7": {
    "inputs": {
      "text": "(low quality:1.3) (((3D render)))",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "8": {
    "inputs": {
      "samples": [
        "17",
        0
      ],
      "vae": [
        "23",
        0
      ]
    },
    "class_type": "VAEDecode"
  },
  "9": {
    "inputs": {
      "filename_prefix": "sdgen/refiner_output",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage"
  },
  "17": {
    "inputs": {
      "seed": 1094187767120321,
      "steps": 10,
      "cfg": 7,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "denoise": 1,
      "model": [
        "4",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "21",
        0
      ]
    },
    "class_type": "KSampler"
  },
  "21": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage"
  },
  "23": {
    "inputs": {
      "vae_name": "sdxl_vae.safetensors"
    },
    "class_type": "VAELoader"
  }
}
"""

def sdxl_exporter(positive_prompt, 
                  negative_prompt, 
                  seed, 
                  width, 
                  height, 
                  batch_size,
                  model_path = None,
                  steps = 10,
                  cfg = 7,
                  sampler_name = "dpmpp_2m",
                  ):
    """Export SDXL prompt"""

    if seed in (None, 0, "", -1):
        seed = random.randint(0, 99999999999999)

    prompt = json.loads(SDXL)
    prompt["6"]["inputs"]["text"] = positive_prompt
    prompt["7"]["inputs"]["text"] = negative_prompt
    prompt["17"]["inputs"]["seed"] = seed
    prompt["17"]["inputs"]["steps"] = steps
    prompt["17"]["inputs"]["cfg"] = cfg
    prompt["17"]["inputs"]["sampler_name"] = sampler_name
    prompt["21"]["inputs"]["width"] = width
    prompt["21"]["inputs"]["height"] = height
    prompt["21"]["inputs"]["batch_size"] = batch_size
    prompt["4"]["inputs"]["ckpt_name"] = model_path if model_path else "SDXL\\dreamshaperXL10_alpha2Xl10.safetensors"
    return prompt
