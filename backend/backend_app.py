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
def manage_posts():
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


def find_post_by_id(post_id):
    """Find the post with the id `post_id`.
    If there is no post with this id, return None."""
    for post in POSTS:
        if post['id'] == post_id:
            return post
    return None


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Find the post with the given ID
    post = find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    # Remove the post from the list
    POSTS.remove(post)

    # Return a message confirming the post was deleted
    return jsonify({"message": "Post deleted", "post": post})


@app.route('/api/posts/<int:id>', methods=['PUT'])
def handle_post(id):
    # Find the post with the given ID
    post = find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return 'Post not found', 404

    # Get the new data
    new_data = request.get_json()

    # Validate the new data
    if not validate_post_data(new_data):
        return jsonify({"error": "Invalid post data"}), 400

    # Update the post with the new data
    post.update(new_data)

    # Return the updated post
    return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search for posts by title or content"""

    # Get the search parameters and strip extra spaces
    title_search = request.args.get('title', '').strip().lower()
    content_search = request.args.get('content', '').strip().lower()
    print (title_search)
    print(content_search)
    # Filter posts by title or content

    title_query = request.args.get('title', '').strip().lower()
    content_query = request.args.get('content', '').strip().lower()

    filtered_posts = [
        post for post in POSTS
        if (title_query and title_query in post['title'].lower()) or
           (content_query and content_query in post['content'].lower())
    ]
    if filtered_posts:
        return jsonify(filtered_posts)
    else:
        return jsonify({"error": "Post not found "}), 404


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return "Title or Content missing"
    if not data["title"].strip() or not data["content"].strip():
        return False
    return True

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
