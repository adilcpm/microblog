from flask import g, jsonify, request, url_for

from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Post


@bp.route('/posts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_post(id):
    return jsonify(Post.query.get_or_404(id).to_dict())

@bp.route('/posts', methods=['GET'])
@token_auth.login_required
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(Post.query.order_by(Post.timestamp.desc()), page, per_page, 'api.get_posts')
    return jsonify(data)

@bp.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    data = request.get_json() or {}
    if 'body' in data:
        new_post = Post(body=data['body'], author=g.current_user)
        db.session.add(new_post)
        db.session.commit()
        response = jsonify(new_post.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.get_post', id=new_post.id)
        return response
    return bad_request('body element not found')
