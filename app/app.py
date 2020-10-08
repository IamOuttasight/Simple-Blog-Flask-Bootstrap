from flask import Flask
from flask_mysqldb import MySQL
from config import Configuration
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Configuration)
mysql = MySQL(app)
csrf = CSRFProtect(app)