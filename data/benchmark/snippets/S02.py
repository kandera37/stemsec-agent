from flask import Flask, request, redirect

app = Flask(__name__)

ALLOWED_PATHS = {"/dashboard", "/profile", "/"}


@app.route("/go")
def go():
    next_url = request.args.get("next", "/")
    if next_url not in ALLOWED_PATHS:
        next_url = "/"
    return redirect(next_url)