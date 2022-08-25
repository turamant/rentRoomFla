from app import app, db

from flask import Flask, request, current_app, session, g, make_response, redirect, abort, render_template

from app.models import Category, Post


@app.before_request
def before_request():
    print("before_request() called")

@app.after_request
def after_request(response):
    print("after_request() called")
    return response


@app.route('/category')
def category_all():
    category = db.session.query(Category).all()
    return render_template('category.html', category=category)


@app.route('/')
def index():
    posts = db.session.query(Post).all()
    return render_template('index.html', posts=posts)


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


