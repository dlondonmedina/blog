from flask import Flask, render_template, request
from .forms import NewEntryForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'us@randomStrin1her0'

@app.route('/')
@app.route('/<name>')
def index(name = None):
   data = {
      'title': 'Fancy-Pants Blog',
      'menu': [
         {
            'link': 'about',
            'text': 'About'
         },
         {
            'link' : 'cv',
            'text': 'CV'
         }, 
         {
            'link' : 'blog',
            'text' : 'Blog'
         }
      ]
   }
   return render_template('index.html', data=data, name=name)


@app.route('/blog')
def blog():
   data = {
      "title": "Fancy-Pants Blog",
      "menu": [
         {
            "link": "about",
            "text": "About"
         },
         {
            "link": "blog",
            "text": "Blog"
         }
      ],
      "posts": [
         {
            "title": "Post One",
            "author": "Jimmy",
            "text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dolor doloremque totam adipisci ex dolores vitae enim soluta quo provident! Voluptatem tenetur harum magni pariatur. Aliquid laborum dolores harum dignissimos quibusdam!"
         },
         {
            "title": "About Chickens",
            "author": "Jimmy",
            "text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dolor doloremque totam adipisci ex dolores vitae enim soluta quo provident! Voluptatem tenetur harum magni pariatur. Aliquid laborum dolores harum dignissimos quibusdam!"
         },
         {
            "title": "Trampled by Turtles",
            "author": "Jimmy",
            "text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dolor doloremque totam adipisci ex dolores vitae enim soluta quo provident! Voluptatem tenetur harum magni pariatur. Aliquid laborum dolores harum dignissimos quibusdam!"
         }
      ]
   }
   return render_template('blog.html', data=data)


@app.route('/post', methods=['GET', 'POST'])
def new_post():
   data = {
      'title': 'Blog',
      'post_title': None,
      'author': None,
      'text': None
   }

   form = NewEntryForm()

   if form.validate_on_submit():
      data['post_title'] = form.data['post_title']
      data['author'] = form.data['author']
      data['text'] = form.data['text']
      form.data['post_title'] = ''
      form.data['author'] = ''
      form.data['text'] = ''

   return render_template('post.html', form=form, data=data)

