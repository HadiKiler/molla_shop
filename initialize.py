from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()
db = SQLAlchemy()# برای جلوگیری از ارور ایمپورت دیبی را در فایل دیگر مسازیم و در فایل اصلی اپ را به ان اضافه میکنیم
