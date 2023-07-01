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
    try:
        r.set(hash, json, ex=time)
        return {"hash":hash, "bool": True, "message": True}
    except redis.RedisError as e:
        error_message = handle_redis_exceptions(e)
        return {"hash":'', "bool": False, "message": str(error_message)}

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

      

def handle_redis_exceptions(exception):
    if isinstance(exception, redis.exceptions.AskError):
        return "ASK error received from Redis cluster."
    elif isinstance(exception, redis.exceptions.AuthenticationError):
        return "Authentication error."
    elif isinstance(exception, redis.exceptions.AuthenticationWrongNumberOfArgsError):
        return "Wrong number of arguments sent to the AUTH command."
    elif isinstance(exception, redis.exceptions.AuthorizationError):
        return "Authorization error."
    elif isinstance(exception, redis.exceptions.BusyLoadingError):
        return "Redis server is still loading the data set."
    elif isinstance(exception, redis.exceptions.ChildDeadlockedError):
        return "Child process is deadlocked after a fork."
    elif isinstance(exception, redis.exceptions.ClusterCrossSlotError):
        return "Keys in the request don't hash to the same slot in Redis cluster."
    elif isinstance(exception, redis.exceptions.ClusterDownError):
        return "Redis cluster is currently down."
    elif isinstance(exception, redis.exceptions.ClusterError):
        return "Cluster errors occurred multiple times."
    elif isinstance(exception, redis.exceptions.ConnectionError):
        return "Error connecting to Redis server."
    elif isinstance(exception, redis.exceptions.DataError):
        return "Data error in Redis operation."
    elif isinstance(exception, redis.exceptions.ExecAbortError):
        return "Execution aborted in Redis."
    elif isinstance(exception, redis.exceptions.InvalidResponse):
        return "Invalid response received from Redis server."
    elif isinstance(exception, redis.exceptions.LockError):
        return "Error acquiring or releasing a lock in Redis."
    elif isinstance(exception, redis.exceptions.LockNotOwnedError):
        return "Lock is not owned and cannot be extended or released."
    elif isinstance(exception, redis.exceptions.MasterDownError):
        return "Master node in Redis cluster is down."
    elif isinstance(exception, redis.exceptions.MaxConnectionsError):
        return "Maximum number of connections to Redis server reached."
    elif isinstance(exception, redis.exceptions.ModuleError):
        return "Error in Redis module."
    elif isinstance(exception, redis.exceptions.MovedError):
        return "MOVED error received from Redis cluster."
    elif isinstance(exception, redis.exceptions.NoPermissionError):
        return "No permission to perform the Redis operation."
    elif isinstance(exception, redis.exceptions.NoScriptError):
        return "Script not found in Redis server."
    elif isinstance(exception, redis.exceptions.OutOfMemoryError):
        return "Redis server has run out of memory."
    elif isinstance(exception, redis.exceptions.PubSubError):
        return "Error in Redis pub/sub operation."
    elif isinstance(exception, redis.exceptions.ReadOnlyError):
        return "Redis server is in read-only mode."
    elif isinstance(exception, redis.exceptions.RedisClusterException):
        return "Redis cluster exception."
    elif isinstance(exception, redis.exceptions.RedisError):
        return "Generic Redis error."
    elif isinstance(exception, redis.exceptions.ResponseError):
        return "Error in Redis response."
    elif isinstance(exception, redis.exceptions.SlotNotCoveredError):
        return "The slot in Redis cluster is not covered."
    elif isinstance(exception, redis.exceptions.TimeoutError):
        return "Timeout error in Redis operation."
    elif isinstance(exception, redis.exceptions.TryAgainError):
        return "TRYAGAIN error received from Redis cluster."
    elif isinstance(exception, redis.exceptions.WatchError):
        return "Error in Redis WATCH operation."
    else:
        return "Unknown Redis error."

