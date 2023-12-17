from flask import Flask, request, jsonify
import json
import secrets
from datetime import datetime

import threading

app = Flask(__name__)

# In-memory storage for posts
posts = {}
lock = threading.Lock()

<<<<<<< HEAD
# Assuming you have a list of users defined somewhere
users = [
    {"id": 1, "username": "user1", "email": "user1@example.com"},
    {"id": 2, "username": "user2", "email": "user2@example.com"}
]

=======
>>>>>>> 0dc3e7e22924cd62fec33dd10ee477921e766102
@app.route('/test_form')
def indexForm():
    return render_template('index.html')

def generate_key():
    return secrets.token_urlsafe(32)

def get_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:   
            return user
    return None

def get_current_timestamp():
    return datetime.utcnow().isoformat()

@app.route('/post', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        msg = data['msg']
        user_id = data['user_id']
        parent_id = data.get('parent_id')
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
            "msg": msg,
            "user_id": user_id,
            "parent_id": parent_id,
            "replies": []
        }

        # Update parent post with the current post ID as a reply
        if parent_id in posts:
            posts[parent_id]["replies"].append(post_id)

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

@app.route('/user/<int:user_id>/posts', methods=['GET'])
def get_posts_by_user(user_id):
    with lock:
        user = get_user_by_id(user_id)

        if user is None:
            return jsonify({"err": "User Not Found"}), 404

        user_posts = [post for post in posts.values() if post.get("user_id") == user_id]

        if not user_posts:
            return jsonify({"msg": "No posts found for the user"}), 200

        formatted_posts = [
            {
                "id": post["id"],
                "timestamp": post["timestamp"],
                "msg": post["msg"],
                "user": user
            }
            for post in user_posts
        ]

        return jsonify(formatted_posts), 200

@app.route('/user', methods=['POST'])
def create_user():
    with lock:
        user_id = len(users) + 1
        user_key = generate_key()
        user = {'id': user_id, 'key': user_key}
        users.append(user)

    return jsonify(user)

@app.route('/posts/date-range', methods=['GET'])
def get_posts_by_date_range():
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        if start_date_str is None and end_date_str is None:
            return jsonify({"err": "At least one of 'start_date' or 'end_date' is required."}), 400

        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S") if start_date_str else None
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S") if end_date_str else None
    except ValueError:
        return jsonify({"err": "Invalid date/time format. Use ISO 8601 format (e.g., '2023-12-31T23:59:59')"}), 400

    with lock:
        filtered_posts = []

        for post in posts.values():
            post_timestamp = datetime.strptime(post["timestamp"], "%Y-%m-%dT%H:%M:%S")

            # Check if the post falls within the specified date range
            if (start_date is None or post_timestamp >= start_date) and (end_date is None or post_timestamp <= end_date):
                filtered_posts.append({
                    "id": post["id"],
                    "timestamp": post["timestamp"],
                    "msg": post["msg"],
                    "user": get_user_by_id(post["user_id"])  # Include user information
                })

        return jsonify(filtered_posts), 200

if __name__ == '__main__':
    app.run(debug=True)
