from database import *
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from decarators import *

@app.route("/")     #Ana Sayfa'dan gelen GET requeste cevap veriyoruz. index.html dosyasını görüntülüyoruz.
def index():
    return render_template("index.html")

@app.route("/fields") #Alanlarımız'dan gelen GET requeste cevap veriyoruz. fields.html dosyasını görüntülüyoruz.
def fields():
    return render_template("fields.html")

@app.route("/staff") #Kadromuz'dan gelen GET requeste cevap veriyoruz. staff.html dosyasını görüntülüyoruz.
def staff():
    return render_template("staff.html")

@app.route("/guidance") #Rehberlik Servisinden'dan gelen GET requeste cevap veriyoruz. guidance.html dosyasını görüntülüyoruz.
def guidance():
    return render_template("guidance.html")

@app.route("/achievements") #Sportif Başarılarımızdan'dan gelen GET requeste cevap veriyoruz. achievements.html dosyasını görüntülüyoruz.
def achievements():
    return render_template("achievements.html")


@app.route("/lessons")
def lessons():
    return render_template("lessons.html")

@app.route("/socialevents")
def socialevents():
    return render_template("socialevents.html")

@app.route("/account")
@login_required
def account():
    return render_template("account.html")
