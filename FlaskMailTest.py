import socks
from app import app
from app import mail
from flask_mail import Message
import smtplib

# socks.set_default_proxy(socks.HTTP, '192.168.33.212')
msg = Message('test subject', sender=app.config['ADMINS'][0], recipients=['bobylev.e.a@gmail.com'])
msg.body = 'example test body'
msg.html = '<h1>HTML Example</h1>'
mail.send(msg)
