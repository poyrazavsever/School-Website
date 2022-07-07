from flask_mysqldb import MySQL
from flask import Flask


UPLOAD_FILE = 'static/uploads'
EXTENSİON = set(['mp4'])
EXTENSİONTWO = set(["png",'txt', 'pdf', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.secret_key = "YusufS"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "YusufS"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['UPLOAD_FOLDER'] = UPLOAD_FILE

mysql = MySQL(app)


