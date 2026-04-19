from flask import Flask, request, session

app = Flask(__name__)


POSTS = {
    1: {"owner_id": 10, "title": "Private draft"},
    2: {"owner_id": 20, "title": "Another private post"},
}


@app.route("/delete_post", methods=["POST"])
def delete_post():
    if "user_id" not in session:
        return "Unauthorized", 401

    post_id = int(request.form["post_id"])
    del POSTS[post_id]

    return "Deleted"