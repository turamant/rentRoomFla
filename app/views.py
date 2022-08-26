from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from app import app, db

from flask import make_response, redirect, render_template

from app.models import Category, Post, Tag, User, Room, Reservation, Review
from mimesis import Person, Text

person = Person('ru')
text = Text('ru')







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
    posts = db.session.query(Post).all()
    tags = db.session.query(Tag).all()
    return render_template('category.html',
                           category=category,
                           posts=posts,
                           tags=tags)



@app.get('/')
def index():
    return render_template('index.html')


class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('admin/any_page/index.html')


class DashBoardView(AdminIndexView):
    @expose('/')
    def add_data_db(self):
        all_users = User.query.all()
        all_rooms = Room.query.all()
        all_reservation = Reservation.query.all()
        return self.render('admin/dashboard_index.html',
                           all_users=all_users,
                           all_rooms=all_rooms,
                           all_reservation=all_reservation)


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


admin = Admin(app, name='Моя программа', template_mode='bootstrap3', index_view=DashBoardView(), endpoint='admin')
admin.add_view(ModelView(User, db.session, name='Пользователь' ))
admin.add_view(ModelView(Room, db.session, name='Недвижимость'))
admin.add_view(ModelView(Reservation, db.session, name='Бронирования'))
admin.add_view(ModelView(Review, db.session, name='Рейтинги'))

