from datetime import datetime

from flask import Flask, request, current_app, session, g, make_response, redirect, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__, template_folder="jinja_templates",  static_folder="static_dir")
app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite100.db'
db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', backref='category')

    def __repr__(self):
        return "<{}:{}>".format(id, self.name)


post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.title[:10])


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', secondary=post_tags, backref='tags')

    def __repr__(self):
        return "<{}:{}>".format(id, self.name)


engine = create_engine('sqlite:///sqlite100.db')
engine.connect()
print(engine)


@app.before_request
def before_request():
    print("before_request() called")

@app.after_request
def after_request(response):
    print("after_request() called")
    return response


@app.route('/')
def index():
    with app.test_request_context('/product/'):
        print(request.path)
        print(request.method)
        print(current_app.name)
        name, age, profession = "Jerry", 24, 'Programmer'
        context = dict(name=name, profession=profession, age=age)
    return render_template('index.html', **context)


@app.route('/resp/')
def make_resp():
    res = make_response("<h2>Ket na kutak</h2>", 200)
    res.headers['Content-Type'] = 'text/plain'
    res.headers['Server'] = 'FooBar'
    print(f"....{res.headers}..{res}.")
    return res


@app.route('/set-cookie/')
def set_cookie():
    res = make_response("Cookie setter")
    res.set_cookie("favorite-color", "blue", 60*60)
    res.set_cookie("favorite-font", "sans-serif", 60*60)
    return res


@app.route('/mark')
def render_markdown():
    return "## Heading", 200, {'Content-Type': 'text/markdown'}


@app.route('/transfer')
def transfer():
    return "", 302, {'location': 'http://localhost:5000/login'}


@app.route('/transfer2')
def transfer2():
    return redirect("http://localhost:5000/login")





@app.errorhandler(404)
def http_404_handler(error):
    return "<p>HTTP 404 Ошибка мдаааааааа</p>", 404

@app.errorhandler(500)
def http_500_handler(error):
    return "<p>HTTP 500 Error Encountered</p>", 500


@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return f"profile page of user #{user_id}"


@app.route('/books/<genre>/')
def books(genre):
    return f"All books in {genre} category."




if __name__ == '__main__':
    app.run(debug=True)