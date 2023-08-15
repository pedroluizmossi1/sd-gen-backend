import configparser
import os
import argparse

parser = argparse.ArgumentParser()
config = configparser.ConfigParser()

config_file_example = """config['REDIS'] = {'redis_host': 'localhost',
                           'redis_port': '6379',
                           'redis_db': '0'}
                         config['MONGODB'] = {'mongodb_host': 'localhost',
                                'mongodb_port': '27017',
                                'mongodb_db': 'main',
                                'mongodb_user': 'root',
                                'mongodb_password': 'password'}
                      """ 


try:
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
except Exception as e:
    print(e)
    exit(1)
else:
    if os.path.exists(os.path.join(os.path.dirname(__file__), 'config.ini')) == False:
        print('Config file not found. Creating new config file...')
        with open(os.path.join(os.path.dirname(__file__), 'config.ini'), 'w') as f:
            f.write(config_file_example)
        config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

def get_config(section, key):
    return config.get(section, key)

def put_config(section, key, value):
    config.set(section, key, value)
    with open(os.path.join(os.path.dirname(__file__), 'config.ini'), 'w') as f:
        config.write(f)

