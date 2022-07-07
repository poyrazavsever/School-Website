from calendar import c
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,abort
from passlib.hash import sha256_crypt

from forms import * # Kayıt ol ve Giriş Yap formu. validators(Kontroller)
from decarators import * # Tekrar giriş yapmayı ve tekrar kayıt olmayı engellemek için decarators.
from database import * # Database bilgilerini tuttuğumuz dosya.

import os
from werkzeug.utils import secure_filename

 #İstenmeyen zararlı dosyaların yüklenmesine engel oluyoruz.
def uzanti_kontrol(file_name):
   return '.' in file_name and \
   file_name.rsplit('.', 1)[1].lower() in EXTENSIONS #Sadece mp4 formatında videolar yüklenebilecek.




@app.route("/upload_lessons", methods = ["POST"])
@login_required
def upload_video_lessons():
   if request.method == "POST":
        
      if 'video_file' not in request.files: # Formdan dosya gelip gelmediğini kontrol edelim.
         flash("Dosya Seçilmedi" , "danger")
         return redirect(url_for('upload_lessons'))

      video_file = request.files(video_file)
      
      if video_file.filename == '':
         flash("Dosya Seçilmedi" , "danger")
         return redirect(url_for('upload_lessons'))

       # gelen dosyayı güvenlik önlemlerinden geçir
      if video_file and uzanti_kontrol(video_file.filename):
         file_name = secure_filename(video_file.filename)
         video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
         #return redirect(url_for('dosyayukleme',dosya=dosyaadi))
         return redirect(url_for('upload_lessons/' + file_name))
   
      else:
         flash('İzin verilmeyen dosya uzantısı!!! Lütfen " .mp4 " uzantılı dosyalar yükleyin.')
         return redirect(url_for('upload_lessons'))
   else:
      abort(401)



   
# Form ile dosya yükleme sayfası
@app.route('/upload_lessons')
@login_required
def upload_lessons():
   form = UploadLessons(request.form)
   return render_template("upload_lessons.html", form = form)



# Form ile dosya yükleme sayfası - Sonuç
@app.route('/upload_lessons/<string:dosya>')
def dosyayuklemesonuc(video_file):
   return render_template("dosyayukleme.html", video_file=video_file)

