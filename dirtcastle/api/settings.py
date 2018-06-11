import os


API_HOST = os.environ.get('API_HOST', '127.0.0.1')
MONGO_HOST = os.environ.get('MONGO_HOST', '127.0.0.1')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_NAME = os.environ.get('MONGO_NAME', 'dirtcastle')
