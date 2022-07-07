from calendar import c
from enum import auto
import fileinput
from unicodedata import name
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,abort
from passlib.hash import sha256_crypt

from forms import * # Kayıt ol ve Giriş Yap formu. validators(Kontroller)
from decarators import * # Tekrar giriş yapmayı ve tekrar kayıt olmayı engellemek için decarators.
from database import * # Database bilgilerini tuttuğumuz dosya.

import os
from werkzeug.utils import secure_filename
import random


name_list = ["A" , "B" , "C" , "D" , "E", "F", "G", "H", "I", "O", "U", "I", "J", "L", "M", "N", "P", "S" ]

def random_name():
   first_n = str(random.randint(1,500))
   second_n = random.choice(name_list)
   third_n = str(random.randint(1,50))
   fourth_n = random.choice(name_list)
   
   c_name = first_n + second_n + third_n + fourth_n +".jpg"
   return c_name



def uzanti_kontrol(dosyaadi):
   return '.' in dosyaadi and \
   dosyaadi.rsplit('.', 1)[1].lower() in EXTENSİONTWO


# Form ile dosya yükleme işlemi
@app.route('/dosyayukle3', methods=['POST'])
def dosyayukle3():
    if request.method == 'POST':

        # formdan dosya gelip gelmediğini kontrol edelim
        if 'dosya' not in request.files:
            flash('Dosya seçilmedi...', "warning")
            return redirect('uploadpictures')         

        # kullanıcı dosya seçmemiş ve tarayıcı boş isim göndermiş mi
        dosya = request.files['dosya']                    
        if dosya.filename == '':
            flash('Dosya seçilmedi...',  "warning")
            return redirect('uploadpictures')

        # gelen dosyayı güvenlik önlemlerinden geçir
        if dosya and uzanti_kontrol(dosya.filename):
            global dosyaadi

            dosyaadi = random_name()
            dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))

            return redirect("uploadpictures")
        else:
            flash('İzin verilmeyen dosya uzantısı!', "danger")
            return redirect('uploadpictures')

    else:
        abort(401)




@app.route("/selectpicture")
@login_required
def selectpicture():
    return render_template("selectpicture.html")

@app.route("/uploadpictures", methods = ["GET", "POST"])
@login_required
def uploadpictures():
    form = UploadPicture(request.form)
    title = form.title.data
    name = session["name"]

    if request.method == "POST" and form.validate():

        path = f"uploads/{dosyaadi}"

        print(path)
        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO photos(author,title,path) VALUES(%s,%s,%s)"
        cursor.execute(sorgu,(name,title,path)) 
        mysql.connection.commit()
        cursor.close()

        flash("Fotoğraf Yayınlandı", "success")
        return redirect("account")

    else:
        return render_template("uploadpictures.html", form = form)