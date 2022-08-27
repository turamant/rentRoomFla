from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func

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


@app.get('/')
def index():
    rooms = db.session.query(Room).all()
    return render_template('index.html', rooms=rooms)


@app.route('/avg-reviews/')
def avg_reviews():

    '''select  room_id, AVG(rating) as avg_score
    from Reservations INNER JOIN Reviews
    ON  Reviews.reservation_id = Reservations.id
    JOIN rooms
	    ON rooms.id=reservations.room_id
    GROUP BY room_id HAVING avg_score;

    Rating.query.with_entities(func.avg(Rating.field2).label('average'))

    reviews = db.session.query(Reservation.room_id, func.avg(Review.rating).label('avg_score'))\
        .join(Review)\
        .group_by(Reservation.room_id)\
        .having(func.avg(Review.rating)).all()
    '''
    reviews = db.session.query(Reservation.room_id, Room.address, func.avg(Review.rating)).select_from(Reservation)\
        .join(Review).filter(Review.reservation_id == Reservation.id)\
        .join(Room).filter(Room.id == Reservation.room_id)\
        .group_by(Reservation.room_id).having(func.avg(Review.rating)).all()
    print("......++...", reviews)
    return render_template('avg_reviews.html', reviews=reviews)


@app.route('/detail_reviews/<int:id>/')
def detail_reviews(id):
    print("...id..= ", id)
    reservation = db.session.query(Reservation).get(id)
    print("....reservation..:>>>..", reservation)
    return render_template('rating_detail.html', reservation=reservation)



@app.route('/ratings/')
def ratings():
    '''
    select rating, address from Reviews
	JOIN Reservations 
		ON reviews.reservation_id=reservations.id
	JOIN rooms
	    ON rooms.id=reservations.room_id;
    '''
    ratings = db.session.query(Review.rating, Room.address).select_from(Review).join(Reservation)\
        .filter(Review.reservation_id == Reservation.id).join(Room).filter(Room.id == Reservation.room_id).all()
    print("...ratings-room:>>>...", ratings)
    return render_template('ratings.html', ratings=ratings)


@app.route('/all-models/')
def all_models():
    users = db.session.query(User).all()
    rooms = db.session.query(Room).join(User).all()
    reservations = db.session.query(Reservation).join(Room).join(User).all()
    print(".....", users)
    reviews = db.session.query(Review).all()
    return render_template('all_models.html',
                           users=users,
                           rooms=rooms,
                           reservations=reservations,
                           reviews=reviews)


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

