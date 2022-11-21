from datetime import datetime
# from flask import jsonify
from itsdangerous import URLSafeTimedSerializer as Serializer
from app import db, ma, login_manager, app
# from flask_marshmallow import fields
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

association_table = db.Table('association_table',
    db.Column('user_id', db.Integer, db.ForeignKey('author.id')),
    db.Column('party_id', db.Integer, db.ForeignKey('party.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=False, nullable=True, default=' ')
    surname = db.Column(db.String(20), unique=False, nullable=True, default=' ')
    phoneNumber = db.Column(db.String(15), unique=False, nullable=True, default=' ')
    location = db.Column(db.String(40), unique=False, nullable=True, default=' ')
    languages = db.Column(db.String(50), unique=False, nullable=True, default=' ')
    image_avatar_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    image_bg_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    party = db.relationship('Party', backref='author', lazy=True)
    attending = db.relationship('Party', secondary=association_table, backref="followers")
    

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}',  '{self.name}', '{self.surname}', '{self.phoneNumber}', '{self.location}', '{self.languages}','{self.image_avatar_file}', '{self.image_bg_file}')"


class Party(db.Model):
    __tablename__ = 'party'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_time = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    lng = db.Column(db.String(30), nullable=False)
    lat = db.Column(db.String(30), nullable=False)
    whatsapp_link = db.Column(db.String(30), nullable=False)
    party_languages = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f"Party('{self.title}', '{self.date_posted}', '{self.date_time}', '{self.address}', '{self.whatsapp_link}', '{self.party_languages}')"

class PartySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Party
        load_instance = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
    party = ma.Nested(PartySchema, many=True)




    
