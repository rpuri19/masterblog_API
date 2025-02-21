from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['GET', 'POST'])
def manage_books():
    if request.method == 'POST':
        # Get the new post data from the client
        new_post = request.get_json()

        # Validate the post data
        if not validate_post_data(new_post):
            return jsonify({"error": "Invalid post data"}), 400

        # Generate a new ID for the post
        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id

        # Add the new post to our list
        POSTS.append(new_post)

        # Return the new post data to the client
        return jsonify(new_post), 201
    else:
        # Handle the GET request
        return jsonify(POSTS)

def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    if not data["title"].strip() or not data["content"].strip():
        return False
    return True


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
