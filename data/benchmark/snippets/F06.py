from flask import Flask

app = Flask(__name__)
app.secret_key = "super_secret_123"


@app.route("/")
def index():
    return "OK"