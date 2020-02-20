import smtplib, ssl
import email

FROM = 'kitseao@yandex.ru'
TO = ['bobylev.e.a@gmail.com']
message = 'body of test email'
body = "\r\n".join((
    "From: bobylev@example.com",
    "To: bobylev@example.com",
    "Subject: test smtpd",
    message
))

# TODO! http://codius.ru/articles/Python_%D0%9A%D0%B0%D0%BA_%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D1%82%D1%8C_%D0%BF%D0%B8%D1%81%D1%8C%D0%BC%D0%BE_%D0%BD%D0%B0_%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D1%83%D1%8E_%D0%BF%D0%BE%D1%87%D1%82%D1%83
smtp_mail_ru = 'smtp.mail.ru'
port_mail_ru = 465
login_mail_ru = 'masternz@mail.ru'
pwd_mail_ru = 'Ujvbhrf1557'

smtp_yandex_ru = 'smtp.yandex.ru'
port_yandex_ru = 465
login_yandex_ru = 'kitseao'
pwd_yandex_ru = 'rbnctfj'
server = None
try:
    server = smtplib.SMTP_SSL(smtp_mail_ru, port=port_mail_ru)
    server.login(login_mail_ru, pwd_mail_ru)
    server.sendmail(FROM, TO, body)
    print('message has sended')
except Exception as ex:
    print(ex)
finally:
    if server is not None:
        server.quit()