from flask import Flask
from get_login_url import get_login_url

server = Flask(__name__)

@server.route("/")
def index():
    return get_login_url()

if __name__ == "__main__":
   server.run(host='0.0.0.0')

