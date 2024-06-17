
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ext import db, login_manager

class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(256), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()


class Product(db.Model, BaseModel):
    __tablename__ = "products"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable= False)
    info = db.Column(db.String(), nullable= False)
    img = db.Column(db.String(), nullable=False, default="default_photo.jpg")
    
    
class User(db.Model, BaseModel, UserMixin):

    __tablename__ = "users"

    id= db.Column(db.Integer(), primary_key=True)
    username= db.Column(db.String())
    password= db.Column(db.String())
    role = db.Column(db.String())

    def __init__(self, username, password, role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
