from functools import wraps
from flask import Flask,flash,redirect,url_for,session

# Kullanıcı giriş decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapınız...","danger")
            return redirect(url_for("login"))
    
    return decorated_function


# Tekrar giriş sayfası gözükmeme

def login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if  not "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Siz zaten giriş yaptınız!","danger")
            return redirect(url_for("index"))
    return decorated_function

#Tekrar kayıt sayfası gözükmeme

def register_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Siz zaten kayıtlısınız!","danger")
            return redirect(url_for("index"))
    return decorated_function