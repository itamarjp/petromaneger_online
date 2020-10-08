import os

MYSQL_HOST = 'localhost'
MYSQL_USER = 'glopessantos'
MYSQL_PASSWORD = 'F100stres'
MYSQL_DB = 'myflaskapp'
MYSQL_CURSORCLASS = 'DictCursor'

CLEAR_DB_MYSQL_HOST = 'us-cdbr-east-02.cleardb.com'
CLEAR_DB_MYSQL_USER = 'b3cc7ed4c109d8'
CLEAR_DB_MYSQL_PASSWORD = '9e6812ed'
CLEAR_DB_MYSQL_DB = 'heroku_62fcb13dd38c297'
CLEAR_DB_MYSQL_CURSORCLASS = 'DictCursor'
executable_path = os.environ.get("CROMEDRIVER_PATH")

MODE = 'development'
