import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # setup connection to SQLite data base
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # configuring admin e-mail
    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USE_TLS = None
    MAIL_USERNAME = 'dotnetcoder@mail.ru'
    MAIL_PASSWORD = 'ujvbhrf1557'
    ADMINS = ['dotnetcoder@mail.ru']
    # pagination
    POSTS_PER_PAGE = 3
