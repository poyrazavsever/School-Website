from cmath import pi
import re
from database import *
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from decarators import *
from forms import UploadPicture, ContactForm
from upload_social import *
import pandas as pd
from flask_mail import Mail

@app.route("/") 
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
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM lessonvideos"
    
    result = cursor.execute(sorgu)
    if result > 0:
        
        videos = cursor.fetchall()

        return render_template("lessons.html", videos = videos)
    else:
        return render_template("lessons.html")



@app.route("/socialevents/videos")
def se_videos():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM socialvideos"
    
    result = cursor.execute(sorgu)
    if result > 0:
        
        videos = cursor.fetchall()

        return render_template("se_videos.html", videos = videos)
    else:
        return render_template("se_videos.html")



@app.route("/socialevents/pictures")
def pictures():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM photos"

    result = cursor.execute(sorgu)
    if result > 0:
        pictures = cursor.fetchall()
        return render_template("se_photos.html", pictures = pictures)
    else:
        return render_template("se_photos.html")

@app.route("/socialevents")
def socialevents():
    return render_template("socialevents.html")



@app.route("/account")
@login_required
def account():
    return render_template("account.html")

@app.route("/account/lesson_video")
@login_required
def my_lesson_video():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM lessonvideos WHERE author = %s "
    result = cursor.execute(sorgu,(session["name"],))
    if result > 0:
        lesson_videos = cursor.fetchall()
            
        return render_template("myl_video.html", lesson_videos = lesson_videos)
    else:
        return render_template("myl_video.html")

@app.route("/account/social_video")
@login_required
def my_social_video():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM socialvideos WHERE author = %s "
    result = cursor.execute(sorgu,(session["name"],))
    if result > 0:
        social_video = cursor.fetchall()
            
        return render_template("mys_video.html",social_video = social_video)
    else:
        return render_template("mys_video.html")


@app.route("/account/social_photo")
@login_required
def my_photo():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM photos WHERE author = %s "
    result = cursor.execute(sorgu,(session["name"],))
    if result > 0:
        photos = cursor.fetchall()
            
        return render_template("mys_photos.html", photos = photos)
    else:
        return render_template("mys_photos.html")


@app.route("/ldelete/<string:id>")
@login_required
def l_delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM lessonvideos WHERE author = %s and ID = %s"
    result = cursor.execute(sorgu, (session["name"], id))

    if result > 0:
        sorgu2 = "DELETE FROM lessonvideos WHERE ID = %s"
        cursor.execute(sorgu2, (id, ))
        mysql.connection.commit()
        flash("Video başarıyla silindi..." , "success")
        return redirect(url_for("account"))
    else:
        flash("Böyle bir video yok ya da sizin bu videoyu silmeye izniniz yok." , "danger")
        return redirect(url_for("account"))


@app.route("/sdelete/<string:id>")
@login_required
def s_delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM socialvideos WHERE author = %s and ID = %s"
    result = cursor.execute(sorgu, (session["name"], id))

    if result > 0:
        sorgu2 = "DELETE FROM socialvideos WHERE ID = %s"
        cursor.execute(sorgu2, (id, ))
        mysql.connection.commit()
        flash("Video başarıyla silindi..." , "success")
        return redirect(url_for("account"))
    else:
        flash("Böyle bir video yok ya da sizin bu videoyu silmeye izniniz yok." , "danger")
        return redirect(url_for("account"))

@app.route("/pdelete/<string:id>")
@login_required
def p_delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM photos WHERE author = %s and ID = %s"
    result = cursor.execute(sorgu, (session["name"], id))

    if result > 0:
        sorgu2 = "DELETE FROM photos WHERE ID = %s"
        cursor.execute(sorgu2, (id, ))
        mysql.connection.commit()
        flash("Fotoğraf başarıyla silindi..." , "success")
        return redirect(url_for("account"))
    else:
        flash("Böyle bir fotoğraf yok ya da sizin bu fotoğrafı silmeye izniniz yok." , "danger")
        return redirect(url_for("account"))



@app.route("/searchl", methods = ["GET", "POST"])
def searchl():
    if request.method == "GET":
        return redirect(url_for("index"))

    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()

        sorgu = "SELECT * FROM lessonvideos WHERE title LIKE '%"+ keyword +"%'"
        result = cursor.execute(sorgu)
        
        if result == 0:
            flash("Aradığınız video bulunamadı...", "warning")
            return redirect("lessons")
        else:
            videos = cursor.fetchall()
            return render_template("lessons.html", videos = videos)



@app.route("/searche", methods = ["GET", "POST"])
def searche():
    
    if request.method == "GET":
        return redirect(url_for("index"))

    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()

        sorgu = "SELECT * FROM socialvideos WHERE title LIKE '%" + keyword + "%'"
        result = cursor.execute(sorgu)

        if result == 0:
            flash("Aradığınız video bulunamadı...", "danger")
            return redirect(url_for("se_videos"))
        else:
            videos = cursor.fetchall()
            return render_template("se_videos.html", videos = videos)
