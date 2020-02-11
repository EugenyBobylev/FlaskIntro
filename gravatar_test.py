# import code for encoding urls and generating md5 hashes
import urllib, hashlib

# Set your variables here
email = "dotnetcoder@mail.ru"
default = "identicon"
size = 40

# construct the url
gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + "?"
gravatar_url += "d=identicon&s=80"

print(gravatar_url)
