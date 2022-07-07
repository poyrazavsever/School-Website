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
   
   c_name = first_n + second_n + third_n + fourth_n +".mp4"
   return c_name


def uzanti_kontrol(dosyaadi):
   return '.' in dosyaadi and \
   dosyaadi.rsplit('.', 1)[1].lower() in EXTENSİON



# Form ile dosya yükleme işlemi
@app.route('/dosyayukle2', methods=['POST'])
def dosyayukle2():

   if request.method == 'POST':

        # formdan dosya gelip gelmediğini kontrol edelim
      if 'dosya' not in request.files:
         flash('Dosya seçilmedi...', "warning")
         return redirect('dosyayukleme2')         

        # kullanıcı dosya seçmemiş ve tarayıcı boş isim göndermiş mi
      dosya = request.files['dosya']                    
      if dosya.filename == '':
         flash('Dosya seçilmedi...',  "warning")
         return redirect('dosyayukleme2')

        # gelen dosyayı güvenlik önlemlerinden geçir
      if dosya and uzanti_kontrol(dosya.filename):
         global dosyaadi
         dosyaadi = random_name()
         dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))

         return redirect("upload_socialevents")
      else:
         flash('İzin verilmeyen dosya uzantısı!', "danger")
         return redirect('dosyayukleme2')

   else:
      abort(401)


# Form ile dosya yükleme sayfası
@app.route('/dosyayukleme2')
def dosyayukleme2():
   return render_template("dosyayukleme2.html")

@app.route("/upload_socialevents", methods = ["GET", "POST"])
def upload_social():
   
   form = UploadsVideo(request.form)

   if request.method == "POST" and form.validate():
      author = session["name"]
      title = form.title.data
      descript = form.description.data
      path = f"uploads/{dosyaadi}"
      cursor = mysql.connection.cursor()
      sorgu = "INSERT INTO socialvideos(author, title, descript, path) VALUES(%s,%s,%s,%s)"
      cursor.execute(sorgu,(author,title,descript,path)) 
      mysql.connection.commit()
      cursor.close()
      
      flash("Video Yayınlandı", "success")
      return redirect("account")
   else:
      return render_template("upload_socialevents.html",  form = form)






