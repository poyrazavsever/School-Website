from flask_mysqldb import MySQL
from flask import Flask


UPLOAD_FOLDER = 'static/videos'  # Filmlerin Yüklendiği Klasör
EXTENSIONS = set(['mp4'])

app = Flask(__name__)

app.secret_key = "YusufS"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "YusufS"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)


