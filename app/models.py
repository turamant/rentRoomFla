import enum
from app import db
from datetime import datetime


class RoomChoicesEnum(enum.Enum):
    kvartira = 'kvartira'
    room = 'komnata'
    house = 'house'


class User(db.Model):
    '''User - сущность клиент'''

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    email_verified_at = db.Column(db.DateTime, default=datetime.utcnow)
    passport = db.Column(db.String(255))
    phone_number = db.Column(db.String(12))
    owner_room = db.relationship('Room', backref='user', cascade='all,delete-orphan')
    reservations = db.relationship('Reservation', backref='user', cascade='all,delete-orphan')

    def __str__(self):
        return self.name


class Room(db.Model):
    '''Room - сущность арендное жилье'''
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    home_type = db.Column(db.Enum(RoomChoicesEnum), default=RoomChoicesEnum.kvartira,
                          nullable=False)
    address = db.Column(db.String(255), nullable=False)
    has_tv = db.Column(db.Boolean)
    has_internet = db.Column(db.Boolean)
    has_kitchen = db.Column(db.Boolean)
    has_air_condition = db.Column(db.Boolean)
    price = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    reservations = db.relationship('Reservation', backref='room', cascade='all,delete-orphan')

    def __str__(self):
        return self.address


class Reservation(db.Model):
    '''Reservation - История бронирования жилья'''

    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Integer)
    total = db.Column(db.Integer)
    reviews = db.relationship('Review', backref='reservations', cascade='all,delete-orphan')

    def __str__(self):
        return str(self.room_id)


class Review(db.Model):
    '''Review - отзывы на арендное жилье'''

    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
    rating = db.Column(db.Integer)

    def __str__(self):
        return str(self.rating)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='category', cascade='all,delete-orphan')

    def __repr__(self):
        return "<{}:{}>".format(id, self.name)


post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.title[:10])


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', secondary=post_tags, backref='tags')

    def __repr__(self):
        return "<{}:{}>".format(id, self.name)