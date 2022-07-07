
from database import * # Database bilgileri ve işlemleri
from router import * # Dizin yolları
from member import * # Giriş yapma ve Kayıt Olma İşlemleri
from upload_lessons import * #Video Yükleme İşlemleri
from upload_social import * #Video Yükleme İşlemleri
from upload_photo import *


if __name__ == "__main__":
    app.run(debug=True)
