from flask import Flask

from routes.user import users_bp
from routes.post import posts_bp
from routes.comment import comments_bp

app = Flask(__name__)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(posts_bp, url_prefix='/posts')
app.register_blueprint(comments_bp, url_prefix='/comments')

if __name__ == '__main__':
    app.run(debug=True)