import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # setup connection to SQLite data base
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # configuring admin e-mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.mail.ru'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USE_SSL = True
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'masternz@mail.ru'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Ujvbhrf1557'
    ADMINS = ['masternz@mail.ru']
    # pagination
    POSTS_PER_PAGE = 3
