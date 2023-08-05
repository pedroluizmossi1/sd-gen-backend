"""Module for comfy sd15 prompt exporter."""
import json
import random


SD15 = r"""
{
  "3": {
    "inputs": {
      "seed": 948551813358952,
      "steps": 20,
      "cfg": 8,
      "sampler_name": "euler",
      "scheduler": "normal",
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
        "5",
        0
      ]
    },
    "class_type": "KSampler"
  },
  "4": {
    "inputs": {
      "ckpt_name": "Artistic\\dreamshaper_8.safetensors"
    },
    "class_type": "CheckpointLoaderSimple"
  },
  "5": {
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage"
  },
  "6": {
    "inputs": {
      "text": "beautiful scenery nature glass bottle landscape, , purple galaxy bottle,",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "7": {
    "inputs": {
      "text": "text, watermark",
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
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode"
  },
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage"
  }
}
"""

def sd15_exporter(positive_prompt, 
                  negative_prompt, 
                  seed, 
                  width, 
                  height, 
                  batch_size,
                  model_path,
                  steps=20,
                  cfg=7,
                  sampler_name="euler"
                  ):
    """Export sd15 prompt."""
    if seed in (None, 0, "", -1):
        seed = random.randint(0, 99999999999999)

    prompt = json.loads(SD15)
    prompt["6"]["inputs"]["text"] = positive_prompt
    prompt["7"]["inputs"]["text"] = negative_prompt
    prompt["3"]["inputs"]["seed"] = seed
    prompt["3"]["inputs"]["steps"] = steps
    prompt["3"]["inputs"]["cfg"] = cfg
    prompt["3"]["inputs"]["sampler_name"] = sampler_name
    prompt["4"]["inputs"]["ckpt_name"] = model_path
    prompt["5"]["inputs"]["width"] = width
    prompt["5"]["inputs"]["height"] = height
    prompt["5"]["inputs"]["batch_size"] = batch_size
    print(json.dumps(prompt, indent=2))
    return prompt

SD15_LATENT = r"""
{
  "3": {
    "inputs": {
      "seed": 918823527510924,
      "steps": 20,
      "cfg": 7,
      "sampler_name": "euler",
      "scheduler": "normal",
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
        "5",
        0
      ]
    },
    "class_type": "KSampler"
  },
  "4": {
    "inputs": {
      "ckpt_name": "Artistic\\dreamshaper_8.safetensors"
    },
    "class_type": "CheckpointLoaderSimple"
  },
  "5": {
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage"
  },
  "6": {
    "inputs": {
      "text": "beautiful scenery nature glass bottle landscape, , purple galaxy bottle,",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "7": {
    "inputs": {
      "text": "text, watermark",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "11",
        0
      ]
    },
    "class_type": "SaveImage"
  },
  "10": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "scale_by": 1.9999999999999984,
      "samples": [
        "3",
        0
      ]
    },
    "class_type": "LatentUpscaleBy"
  },
  "11": {
    "inputs": {
      "samples": [
        "12",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode"
  },
  "12": {
    "inputs": {
      "seed": 935692868641138,
      "steps": 20,
      "cfg": 7,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 0.49999999999999956,
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
        "10",
        0
      ]
    },
    "class_type": "KSampler"
  }
}
"""

def sd15_latent_exporter(positive_prompt, 
                  negative_prompt, 
                  seed, 
                  width, 
                  height, 
                  batch_size,
                  model_path,
                  steps=20,
                  cfg=7,
                  sampler_name="euler",
                  latent_denoise = 0.5,
                  latent_seed = -1,
                  latent_steps=20,
                  latent_cfg=7,
                  latent_sampler_name="euler"
                  ):
    """Export sd15 prompt."""
    if seed in (None, 0, "", -1):
        seed = random.randint(0, 99999999999999)
    if latent_seed in (None, 0, "", -1):
        latent_seed = random.randint(0, 99999999999999)

    prompt = json.loads(SD15_LATENT)
    prompt["6"]["inputs"]["text"] = positive_prompt
    prompt["7"]["inputs"]["text"] = negative_prompt
    prompt["3"]["inputs"]["seed"] = seed
    prompt["3"]["inputs"]["steps"] = steps
    prompt["3"]["inputs"]["cfg"] = cfg
    prompt["3"]["inputs"]["sampler_name"] = sampler_name
    prompt["4"]["inputs"]["ckpt_name"] = model_path
    prompt["5"]["inputs"]["width"] = width
    prompt["5"]["inputs"]["height"] = height
    prompt["5"]["inputs"]["batch_size"] = batch_size
    prompt["12"]["inputs"]["seed"] = latent_seed
    prompt["12"]["inputs"]["steps"] = latent_steps
    prompt["12"]["inputs"]["cfg"] = latent_cfg
    prompt["12"]["inputs"]["sampler_name"] = latent_sampler_name
    prompt["12"]["inputs"]["denoise"] = latent_denoise
    return prompt