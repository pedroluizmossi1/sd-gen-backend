import redis
from crypto_dash.crypto_core import generate_hash
from fastapi import HTTPException
import json
from config_core import get_config

host = get_config('REDIS', 'redis_host')
port = get_config('REDIS', 'redis_port')
db = get_config('REDIS', 'redis_db')
user = get_config('REDIS', 'redis_user')
password = get_config('REDIS', 'redis_password')

r = redis.Redis(host=host, port=port, decode_responses=True, db=db, username=user, password=password)

def insert_json(json, time):
    hash = generate_hash()
    try:
        r.set(hash, json, ex=time)
        return hash
    except redis.RedisError as e:
        error_message = handle_redis_exceptions(e)
        raise HTTPException(status_code=500, detail=str(error_message))

def get_json(hash):
    try:
        json = r.get(hash)
        return json
    except redis.RedisError as e:
        error_message = handle_redis_exceptions(e)
        raise HTTPException(status_code=500, detail=str(error_message))

def delete_json(hash):
    try:
        r.delete(hash)
        return True
    except redis.RedisError as e:
        error_message = handle_redis_exceptions(e)
        raise HTTPException(status_code=500, detail=str(error_message))
    
def get_all_string_values(value):
    try:
        keys = r.scan_iter('*')
        values = []
        for key in keys:
            data = r.get(key)
            if data:
                json_data = json.loads(data)
                if isinstance(json_data, dict) and 'login' in json_data and json_data['login'] == value:
                    values.append(key)
        return values
    except redis.RedisError as e:
        error_message = handle_redis_exceptions(e)
        raise HTTPException(status_code=500, detail=str(error_message))

def delete_all_string_values(value):
    try:
        keys = r.scan_iter('*')
        for key in keys:
            data = r.get(key)
            if data:
                json_data = json.loads(data)
                if isinstance(json_data, dict) and 'login' in json_data and json_data['login'] == value:
                    r.delete(key)
        return True
    except redis.RedisError as e:
        error_message = handle_redis_exceptions(e)
        raise HTTPException(status_code=500, detail=str(error_message))


def insert_hash(hash, value, time):
    try:
        r.hmset(hash, value)
        r.expire(hash, time)
        return True
    except redis.RedisError as e:
        error_message = handle_redis_exceptions(e)
        raise HTTPException(status_code=500, detail=str(error_message))
    
def get_hash(hash):	
    try:
        value = r.hgetall(hash)
        return value
    except redis.RedisError as e:
        error_message = handle_redis_exceptions(e)
        raise HTTPException(status_code=500, detail=str(error_message))
    
def delete_hash(hash):
    try:
        r.delete(hash)
        return True
    except redis.RedisError as e:
        error_message = handle_redis_exceptions(e)
        raise HTTPException(status_code=500, detail=str(error_message))

def handle_redis_exceptions(exception):
    if isinstance(exception, redis.exceptions.AskError):
        raise HTTPException(status_code=500, detail="ASK error in Redis.")
    elif isinstance(exception, redis.exceptions.AuthenticationError):
        raise HTTPException(status_code=500, detail="Authentication error.")
    elif isinstance(exception, redis.exceptions.AuthenticationWrongNumberOfArgsError):
        raise HTTPException(status_code=500, detail="Wrong number of arguments sent to the AUTH command.")
    elif isinstance(exception, redis.exceptions.AuthorizationError):
        raise HTTPException(status_code=500, detail="Authorization error.")
    elif isinstance(exception, redis.exceptions.BusyLoadingError):
        raise HTTPException(status_code=500, detail="Redis server is still loading the data set.")
    elif isinstance(exception, redis.exceptions.ChildDeadlockedError):
        raise HTTPException(status_code=500, detail="Child process is deadlocked after a fork.")
    elif isinstance(exception, redis.exceptions.ClusterCrossSlotError):
        raise HTTPException(status_code=500, detail="Keys in the request don't hash to the same slot in Redis cluster.")
    elif isinstance(exception, redis.exceptions.ClusterDownError):
        raise HTTPException(status_code=500, detail="Redis cluster is currently down.")
    elif isinstance(exception, redis.exceptions.ClusterError):
        raise HTTPException(status_code=500, detail="Cluster errors occurred multiple times.")
    elif isinstance(exception, redis.exceptions.ConnectionError):
        raise HTTPException(status_code=500, detail="Error connecting to Redis server.")
    elif isinstance(exception, redis.exceptions.DataError):
        raise HTTPException(status_code=500, detail="Data error in Redis operation.")
    elif isinstance(exception, redis.exceptions.ExecAbortError):
        raise HTTPException(status_code=500, detail="Execution aborted in Redis.")
    elif isinstance(exception, redis.exceptions.InvalidResponse):
        raise HTTPException(status_code=500, detail="Invalid response received from Redis server.")
    elif isinstance(exception, redis.exceptions.LockError):
        raise HTTPException(status_code=500, detail="Error acquiring or releasing a lock in Redis.")
    elif isinstance(exception, redis.exceptions.LockNotOwnedError):
        raise HTTPException(status_code=500, detail="Lock is not owned and cannot be extended or released.")
    elif isinstance(exception, redis.exceptions.MasterDownError):
        raise HTTPException(status_code=500, detail="Master node in Redis cluster is down.")
    elif isinstance(exception, redis.exceptions.MaxConnectionsError):
        raise HTTPException(status_code=500, detail="Maximum number of connections to Redis server reached.")
    elif isinstance(exception, redis.exceptions.ModuleError):
        raise HTTPException(status_code=500, detail="Error in Redis module.")
    elif isinstance(exception, redis.exceptions.MovedError):
        raise HTTPException(status_code=500, detail="MOVED error received from Redis cluster.")
    elif isinstance(exception, redis.exceptions.NoPermissionError):
        raise HTTPException(status_code=500, detail="No permission to perform the Redis operation.")
    elif isinstance(exception, redis.exceptions.NoScriptError):
        raise HTTPException(status_code=500, detail="Script not found in Redis server.")
    elif isinstance(exception, redis.exceptions.OutOfMemoryError):
        raise HTTPException(status_code=500, detail="Redis server has run out of memory.")
    elif isinstance(exception, redis.exceptions.PubSubError):
        raise HTTPException(status_code=500, detail="Error in Redis pub/sub operation.")
    elif isinstance(exception, redis.exceptions.ReadOnlyError):
        raise HTTPException(status_code=500, detail="Redis server is in read-only mode.")
    elif isinstance(exception, redis.exceptions.RedisClusterException):
        raise HTTPException(status_code=500, detail="Redis cluster exception.")
    elif isinstance(exception, redis.exceptions.RedisError):
        raise HTTPException(status_code=500, detail="Generic Redis error.")
    elif isinstance(exception, redis.exceptions.ResponseError):
        raise HTTPException(status_code=500, detail="Error in Redis response.")
    elif isinstance(exception, redis.exceptions.SlotNotCoveredError):
        raise HTTPException(status_code=500, detail="The slot in Redis cluster is not covered.")
    elif isinstance(exception, redis.exceptions.TimeoutError):
        raise HTTPException(status_code=500, detail="Timeout error in Redis operation.")
    elif isinstance(exception, redis.exceptions.TryAgainError):
        raise HTTPException(status_code=500, detail="TRYAGAIN error received from Redis cluster.")
    elif isinstance(exception, redis.exceptions.WatchError):
        raise HTTPException(status_code=500, detail="Error in Redis WATCH operation.")
    else:
        raise HTTPException(status_code=500, detail="Unknown Redis error.")

