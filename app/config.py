class Configuration:
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'toor' # Set your MySQL password here
    MYSQL_DB = 'simple_blog'
    MYSQL_CURSORCLASS = 'DictCursor'
    SECRET_KEY = 'super-secret-key' # Set your own secret key