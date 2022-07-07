from wtforms import Form,StringField,TextAreaField,PasswordField, form, meta,validators
from passlib.hash import sha256_crypt
from wtforms.widgets import TextArea


# Kullanıcı Kayıt Formu
class RegisterForm(Form):

    code = StringField("")
    name = StringField("",validators = [validators.length(min = 4,max= 16)])
    email = StringField("",validators = [validators.Email(message="Lütfen Geçerli Bir Email Adresi Giriniz")])
    password = PasswordField("",validators=[

        validators.DataRequired(message="Lütfen bir parola giriniz"),
        validators.EqualTo(fieldname = "confirm",message = "Parolanız Uyuşmuyor...")
    
    ])
    confirm = PasswordField("")


#Kullanıcı Giriş Formu
class LoginForm(Form):

    name = StringField("")
    password = PasswordField("")

#Öğretmenlerin Dersler adı altında video yüklemesi için Form

class UploadLessons(Form):
    
    name = StringField("", validators= [validators.length(min = 6, max = 16)])
    description = TextAreaField("", validators= [validators.length(min = 30, max = 150)], render_kw={"rows" :10,"cols" : 20})


