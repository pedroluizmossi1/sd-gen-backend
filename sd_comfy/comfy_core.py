import time
import uuid
import json
import urllib.request
import urllib.parse
import websockets
import asyncio
from config_core import get_config

server_address_list = get_config('COMFYUI', 'comfyui_servers').split(',')

def get_server_config(server_index=None):
    if server_index is not None:
        return server_address_list[server_index]
    return server_address_list[0]

async def async_ws_connect(user_id, server_index=None):
    server_address = get_server_config(server_index)
    uri = f"ws://{server_address}/ws?clientId={user_id}"
    print(f"Connecting to {uri}")
    websocket = await websockets.connect(uri)
    await asyncio.sleep(0.1)  # Allow some time for the WebSocket connection to stabilize
    return websocket

def queue_prompt(prompt, client_id, server_address):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type, server_address):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()

def get_history(prompt_id, server_address):
    with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())

def get_queue(user_id=None, server_index=None):
    server_address = get_server_config(server_index)
    with urllib.request.urlopen(f"http://{server_address}/queue") as response:
        queue_data = json.loads(response.read())
        queue_running = queue_data.get("queue_running", [])
        queue_pending = queue_data.get("queue_pending", [])
        queue_position = queue_data.get("queue_pending", [])
        queue_position_size = queue_data.get("queue_pending", [])
        if user_id is not None:
            try:
                queue_running = [item for item in queue_running if item[3]["client_id"] == user_id]
            except:
                queue_running = []
            try:
                queue_position = [item for item in queue_pending if item[3]["client_id"] == user_id]
                queue_position_size = sorted([item[0] for item in queue_pending], reverse=False)
                for i in range(len(queue_position)):
                    queue_position[i] = queue_position[i][0]       
            except:
                queue_position = []
        queue_running_len = len(queue_running)
        queue_pending_len = len(queue_pending)
        queue_position = queue_position_size.index(queue_position[0]) + 1 if queue_position else 0
        return {"queue_running": queue_running_len, 
                "queue_pending": queue_pending_len, 
                "queue_position": queue_position}

async def get_images(ws, prompt, client_id, server_address):
    prompt_id = queue_prompt(prompt, client_id, server_address)['prompt_id']
    print(prompt_id)
    output_images = {}
    while True:
        out = await ws.recv()
        #if isinstance(out, str):
        message = json.loads(out)
        if message['type'] == 'executing':
            data = message['data']
            if data['node'] is None and data['prompt_id'] == prompt_id:
                break  # Execution is done
        else:
            continue  # previews are binary data

    history = get_history(prompt_id, server_address)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'], server_address)
                    images_output.append(image_data)
                output_images = images_output

    return output_images

async def async_get_images(prompt, client_id, server_index=None):
    server_address = get_server_config(server_index)
    ws = await async_ws_connect(client_id, server_index)
    try:
        print(server_address)
        images = await get_images(ws, prompt, client_id, server_address)
    finally:
        await ws.close()
    return images

async def get_queue_async(user_id=None, server_index=None):
    loop = asyncio.get_event_loop()
    queue = await loop.run_in_executor(None, get_queue, user_id, server_index)
    return queue
