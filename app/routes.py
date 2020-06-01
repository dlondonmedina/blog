from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import NewEntryForm, LoginForm, RegistrationForm
from app.models import User, Post 

@app.route('/')
def index():
   title = 'Fancy-Pants Blog'
   return render_template('index.html', title=title)


@app.route('/blog')
@app.route('/blog/<id>')
def blog(id=None):
   title = 'Fancy-Pants Blog'
   if id is None:
      data = Post.query.order_by('created')
   else:
      data = [Post.query.filter_by(id=id).first_or_404()]
   
   return render_template('blog.html', title=title, data=data)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def new_post():

   form = NewEntryForm()
   if form.validate_on_submit():
      p = Post(
         title = form.post_title.data,
         slug = form.slug.data,
         body = form.text.data,
         author = current_user.id
      )
      db.session.add(p)
      db.session.commit()
      flash('Post Created!')
      return redirect(url_for('blog'))
   return render_template('post.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = LoginForm()
   if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()
      if user is None:
         flash('Invalid Email.')
         return redirect(url_for('login'))
      if not user.check_password(form.password.data):
         flash('Invalid Password.')
         return redirect(url_for('login'))
      login_user(user, remember=form.remember_me.data)
      flash('You were successfully logged in.')
      return redirect(url_for('index'))
   return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
   logout_user()
   flash('You are logged out.')
   return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = RegistrationForm()
   if form.validate_on_submit():
           
      user = User(
         username=form.username.data,
         email = form.email.data,
         first_name = form.first.data,
         last_name = form.last.data
      )

      user.hash_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      flash('Thanks for registering!')
      return redirect(url_for('login'))
   return render_template('register.html', title='Register', form=form)

