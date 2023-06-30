import redis
from crypto_dash.crypto_core import generate_hash
import json
from config_core import get_config

host = get_config('REDIS', 'redis_host')
port = get_config('REDIS', 'redis_port')
db = get_config('REDIS', 'redis_db')

r = redis.Redis(host=host, port=port, decode_responses=True, db=db)

def insert_json(json, time):
    hash = generate_hash()
    r.set(hash, json, ex=time)
    return hash

def get_json(hash):
    try:
        json = r.get(hash)
        return json
    except:
        return False

def delete_json(hash):
    try:
        r.delete(hash)
        return True
    except:
        return False
    
def get_all_string_values(value):
    keys = r.scan_iter('*')
    values = []
    for key in keys:
        data = r.get(key)
        if data:
            json_data = json.loads(data)
            if isinstance(json_data, dict) and 'login' in json_data and json_data['login'] == value:
                values.append(key)
    return values

def delete_all_string_values(value):
    keys = r.scan_iter('*')
    for key in keys:
        data = r.get(key)
        if data:
            json_data = json.loads(data)
            if isinstance(json_data, dict) and 'login' in json_data and json_data['login'] == value:
                r.delete(key)
    return True

      

