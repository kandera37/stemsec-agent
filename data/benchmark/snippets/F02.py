from flask import Flask, request, render_template_string

app = Flask(__name__)


@app.route("/search")
def search():
    query = request.args.get("q", "")
    return render_template_string(f"<h1>Search results for: {query}</h1>")