import redis
from crypto_dash.crypto_core import generate_hash
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)

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
      

