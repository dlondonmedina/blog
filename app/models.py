from . import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from app import login

class User(UserMixin, db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(40), index=True, unique=True, nullable=False)
   email = db.Column(db.String(120), index=True, unique=True, nullable=False)
   first_name = db.Column(db.String(120), nullable=False)
   last_name = db.Column(db.String(120), nullable=False)
   password = db.Column(db.String(200))
   joined = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
   posts = db.relationship('Post', backref='author_posts', lazy='dynamic')

   def hash_password(self, password):
      self.password = generate_password_hash(password, method='sha256')

   def check_password(self, password):
      return check_password_hash(self.password, password)

   def __repr__(self):
      return '<User {}>'.format(self.username)


class Post(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(120), nullable=False)
   slug = db.Column(db.String(140), nullable=False)
   body = db.Column(db.Text(), nullable=False)
   created = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
   author = db.Column(db.Integer, db.ForeignKey('user.id'))

   def __repr__(self):
      return '<Post> {}'.format(self.slug)


@login.user_loader
def load_user(id):
   return User.query.get(int(id))
