import smtplib
from email.header import Header

import socks
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO! http://codius.ru/articles/Python_%D0%9A%D0%B0%D0%BA_%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D1%82%D1%8C_%D0%BF%D0%B8%D1%81%D1%8C%D0%BC%D0%BE_%D0%BD%D0%B0_%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D1%83%D1%8E_%D0%BF%D0%BE%D1%87%D1%82%D1%83
smtp_mail_ru = 'smtp.mail.ru'
port_mail_ru = 465
login_mail_ru = 'masternz@mail.ru'
pwd_mail_ru = 'Ujvbhrf1557'

addr_from = login_mail_ru
addr_to = 'bobylev.e.a@gmail.com'

msg = MIMEMultipart()
msg['From'] = addr_from
msg['To'] = addr_to
msg['Subject'] = 'Проверка отравленного сообщения'
body = 'Данное письмо было направлено в тестовых целях'
msg.attach(MIMEText(body, 'plain', 'utf-8'))

html = """
<html>
  <head></head>
  <body>
    <p>Фрагмент кода html</p>
  </body>
</html>
"""
msg.attach(MIMEText(html, 'html', 'utf-8'))

# socks.set_default_proxy(socks.HTTP, '192.168.33.212', 8080)
# socks.wrapmodule(smtplib)
server = None
try:
    server = smtplib.SMTP_SSL(host=smtp_mail_ru, port=port_mail_ru)
    server.login(login_mail_ru, pwd_mail_ru)
    server.sendmail(addr_from, addr_to, msg.as_string())
    print('message has sended')
except Exception as ex:
    print(f'Error="{ex}"')
finally:
    if server is not None:
        server.quit()