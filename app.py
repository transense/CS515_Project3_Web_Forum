from flask import Flask, request, jsonify
import json
import secrets
import datetime
import threading

app = Flask(__name__)

# In-memory storage for posts
posts = {}
lock = threading.Lock()

def generate_key():
    return secrets.token_urlsafe(32)

def get_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            return user
    return None

def get_post_by_id(post_id):
    for post in posts:
        if post['id'] == post_id:
            return post
    return None

def get_current_timestamp():
    return datetime.datetime.utcnow().isoformat()

@app.route('/post', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        msg = data['msg']
    except (json.JSONDecodeError, KeyError):
        return jsonify({"err": "Bad Request"}), 400

    with lock:
        post_id = len(posts) + 1
        key = generate_key()
        timestamp = get_current_timestamp()

        posts[post_id] = {
            "id": post_id,
            "key": key,
            "timestamp": timestamp,
            "msg": msg
        }

    return jsonify({
        "id": post_id,
        "key": key,
        "timestamp": timestamp
    })

@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    with lock:
        if post_id not in posts:
            return jsonify({"err": "Not Found"}), 404

        post = posts[post_id]
        return jsonify({
            "id": post["id"],
            "timestamp": post["timestamp"],
            "msg": post["msg"]
        })

@app.route('/post/<int:post_id>/delete/<key>', methods=['DELETE'])
def delete_post(post_id, key):
    with lock:
        if post_id not in posts:
            return jsonify({"err": "Not Found"}), 404

        post = posts[post_id]
        if key != post["key"]:
            return jsonify({"err": "Forbidden"}), 403

        del posts[post_id]

    return jsonify({
        "id": post["id"],
        "key": post["key"],
        "timestamp": post["timestamp"]
    })

if __name__ == '__main__':
    app.run(debug=True)
