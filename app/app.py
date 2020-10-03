from flask import Flask
from flask_mysqldb import MySQL
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
mysql = MySQL(app)