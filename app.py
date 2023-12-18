from flask import Flask, request, jsonify
import datetime
import secrets
import threading

app = Flask(__name__)

posts = {}
users = {}
lock = threading.Lock()

@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user_id = len(users) + 1
        user_key = secrets.token_hex(16)
        unique_metadata = data['unique_metadata']
        non_unique_metadata = data.get('non_unique_metadata', '')

        with lock:
            users[user_id] = {
                'id': user_id,
                'key': user_key,
                'unique_metadata': unique_metadata,
                'non_unique_metadata': non_unique_metadata
            }

        return jsonify({'id': user_id, 'key': user_key}), 201

    except (KeyError, ValueError) as e:
        return jsonify({'err': str(e)}), 400

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_metadata(user_id):
    with lock:
        if user_id not in users:
            return jsonify({'err': 'User not found'}), 404

        user = users[user_id]
        return jsonify({'id': user['id'], 'unique_metadata': user['unique_metadata']}), 200

@app.route('/user/<int:user_id>/edit', methods=['PUT'])
def edit_user_metadata(user_id):
    try:
        data = request.get_json()
        user_key = data['key']
        new_metadata = data['new_metadata']

        with lock:
            if user_id not in users:
                return jsonify({'err': 'User not found'}), 404

            user = users[user_id]

            if user_key != user['key']:
                return jsonify({'err': 'Forbidden'}), 403

            # Update user metadata
            user['unique_metadata'] = new_metadata

            return jsonify({'id': user['id'], 'unique_metadata': user['unique_metadata']}), 200

    except (KeyError, ValueError) as e:
        return jsonify({'err': str(e)}), 400

@app.route('/post', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        msg = data['msg']
        user_id = data['user_id']
        user_key = data['user_key']
        reply_to = data.get('reply_to', None)

        with lock:
            # Create unique ID and key
            post_id = len(posts) + 1
            post_key = secrets.token_hex(16)  # Generate a 32-character (16 bytes) random key

            # Create timestamp
            timestamp = datetime.datetime.utcnow().isoformat()

            # Create post
            posts[post_id] = {
                'id': post_id,
                'key': post_key,
                'timestamp': timestamp,
                'msg': msg,
                'user_id': user_id,
                'reply_to': reply_to
            }

            # Return response
            return jsonify({'id': post_id, 'key': post_key, 'timestamp': timestamp}), 201

    except (KeyError, ValueError) as e:
        return jsonify({'err': str(e)}), 400

@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    with lock:
        if post_id not in posts:
            return jsonify({'err': 'Post not found'}), 404

        post = posts[post_id]

        # Include the id of the post to which it is replying
        reply_to_id = post.get('reply_to', None)
        reply_to_info = {'reply_to': reply_to_id} if reply_to_id else {}

        # Include the ids of every reply to that post
        replies = [pid for pid, pdata in posts.items() if pdata.get('reply_to') == post_id]
        replies_info = {'replies': replies} if replies else {}

        return jsonify({'id': post['id'], 'timestamp': post['timestamp'], 'msg': post['msg'],
                        'user_id': post['user_id'], **reply_to_info, **replies_info}), 200

@app.route('/posts/search', methods=['GET'])
def search_posts_by_datetime():
    try:
        start_datetime = request.args.get('start_datetime')
        end_datetime = request.args.get('end_datetime')

        with lock:
            filtered_posts = []

            for post_id, post_data in posts.items():
                post_timestamp = datetime.datetime.fromisoformat(post_data['timestamp'])

                if (start_datetime is None or post_timestamp >= datetime.datetime.fromisoformat(start_datetime)) and \
                        (end_datetime is None or post_timestamp <= datetime.datetime.fromisoformat(end_datetime)):
                    filtered_posts.append({
                        'id': post_data['id'],
                        'timestamp': post_data['timestamp'],
                        'msg': post_data['msg'],
                        'user_id': post_data['user_id']
                    })

            return jsonify(filtered_posts), 200

    except ValueError:
        return jsonify({'err': 'Invalid datetime format'}), 400



if __name__ == '__main__':
    app.run(debug=True)
