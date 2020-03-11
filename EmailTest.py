import smtplib
from email.header import Header

import socks
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO!
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

socks.set_default_proxy(socks.HTTP, '192.168.33.212', 8080)
socks.wrapmodule(smtplib)
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