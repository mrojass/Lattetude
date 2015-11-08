import os

from flask import Flask, render_template, request, url_for, abort
from models import db, User

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
INSTANCE_FOLDER_PATH = os.path.join(PROJECT_PATH, 'tmp/instance')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/db.sqlite'
app.config['SECRET_KEY'] = '\x0c^\xce\x17i\xa9\x18+\xf5\x91\xac\xb3\x90\xd5\x8f\xed\xda\x8b\x82\xe5\xcd\xdaZ\xc0'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<username>')
def user_profile(username):
    return "Hello, " + username


@app.route('/user/<username>/post')
def create_post(username):
    return "Form to make a post"


@app.route('/post/<int:post_id>')
def list_post_results(post_id):
    return "List comments for post"


@app.route('/_get_facebook_login', methods=['GET', 'POST'])
def get_facebook_login():
    facebook_id = request.values['facebook_id']
    name = request.values['name']
    if facebook_id:
        user = User.query.filter_by(facebook_id=facebook_id).first()
        if not user:
            user = User(facebook_id, name)
            db.session.add(user)
            db.session.commit()
        return url_for('user_profile', username=user.username)
    return abort(403)


if __name__ == "__main__":
    app.run(debug=True)
