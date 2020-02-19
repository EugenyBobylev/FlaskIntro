import smtplib
import email

FROM = 'bobylev@example.com'
TO = ['bobylev@example.com']
message = 'body of test email'
body = "\r\n".join((
    "From: bobylev@example.com",
    "To: bobylev@example.com",
    "Subject: test smtpd",
    message
))
server = smtplib.SMTP('localhost:8025')
server.sendmail(FROM, TO, body)