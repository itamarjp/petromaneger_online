import os

def get_env(key,default=None):
   return os.getenv(key,default)


MYSQL_HOST = get_env('MYSQL_HOST', 'localhost')
MYSQL_USER = get_env('MYSQL_USER', 'glopessantos')
MYSQL_PASSWORD = get_env('MYSQL_PASSWORD', 'F100stres')
MYSQL_DB = get_env('MYSQL_DB', 'myflaskapp')
MYSQL_CURSORCLASS = get_env('MYSQL_CURSORCLASS', 'DictCursor')
executable_path = get_env('CROMEDRIVER_PATH', '')
MODE = get_env('MODE', 'development')
FLASK_DEBUG = get_env('FLASK_DEBUG', '1')
SECRET_KEY =  get_env('SECRET_KEY', 'secret_key_123')