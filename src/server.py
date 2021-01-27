from flask import Flask, request, render_template
import requests 
from urllib.parse import unquote
from get_login_url import get_login_url

"""

Caution:

This code is to demonstrate Server-Side Request Forgery, 
it would leake the ec2 credential to the public.

Do NOT run this code in any ec2 instance without understanding IMDS. 

"""

server = Flask(__name__)

@server.route("/url")
def login_url():
    return get_login_url()


@server.route("/", methods = ["GET", "POST"])
def proxy():
    if request.method == "POST":
        request_url = request.form.get('url')
        r = requests.get(request_url)
        return render_template("form.html", url=request_url,  contents=r.text) 
    
    return render_template("form.html") 

if __name__ == "__main__":
   server.run(host='localhost', port=8080)

