from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from passlib.hash import sha256_crypt

from forms import * # Kayıt ol ve Giriş Yap formu. validators(Kontroller)
from decarators import * # Tekrar giriş yapmayı ve tekrar kayıt olmayı engellemek için decarators.
from database import * # Database bilgilerini tuttuğumuz dosya.



#Kayıt olma işlemi
@app.route("/register",methods = ["GET","POST"])
@register_req
def register():
    
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        real_code = "DENEME1"
        code = form.code.data
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()
        sorgu = "Insert into teachers(name,email,password) Values(%s,%s,%s)"
        if real_code == code:
            cursor.execute(sorgu,(name,email,password))
            mysql.connection.commit()
            cursor.close()
            flash("Başarıyla Kayıt Oldunuz!" , "success")
            return redirect(url_for("login"))

        else:
            flash("Kodu yanlış girdiniz. Lütfen tekrar deneyin..." , "danger")
            return redirect(url_for("register"))
    else:
        
        return render_template("register.html",form = form)


#Giriş Yapma İşlemi

@app.route("/login",methods = ["GET","POST"])
@login_req
def login():
    form = LoginForm(request.form)
    
    if request.method == "POST":
        name = form.name.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()
        
        sorgu = "SELECT * FROM teachers WHERE name = %s"
        result = cursor.execute(sorgu,(name,))

        if result > 0 :
            data = cursor.fetchone()
            real_password = data["password"]

            if sha256_crypt.verify(password_entered,real_password):
                flash("Başarıyla giriş yapıldı...","success")

                session["logged_in"] = True
                session["name"] = name

                return redirect(url_for("index"))
            else:
                flash("Parolanızı yanlış girdiniz...","danger")
                return redirect(url_for("login"))

        else:
            flash("Böyle bir kullanıcı bulunmuyor...", "danger")
            return redirect(url_for("login"))

    return render_template("login.html",form = form)


#Çıkış Yapma İşlemi
@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))



