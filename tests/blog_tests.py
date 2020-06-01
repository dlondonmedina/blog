import os 
from bs4 import BeautifulSoup

import unittest
from app import app, db
from app.models import User, Post 

# Global Test database
TEST_DB = 'test.db'

class TestBlog(unittest.TestCase):
   @classmethod
   def setUpClass(cls):
      app.config['TESTING'] = True
      app.config['WTF_CSRF_ENABLED'] = False
      app.config['DEBUG'] = False
      app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
         os.path.join(app.config['BASE_DIR'], TEST_DB)
      db.create_all()

   @classmethod 
   def tearDownClass(cls):
      db.drop_all()

   def setUp(self):
      
      self.client = app.test_client()
      
      # Add a test user
      u = User(username='author', email='author@example.com', 
                  first_name='Author', last_name='McAuthorson')
      u.hash_password('password')
      db.session.add(u)
      db.session.commit()
      u1 = User.query.get(1)

      # # Add 2 test posts
      p1 = Post(title='Title', slug='Sluggy', body='The body text.', author=u1.id)
      db.session.add(p1)
      db.session.commit()
      p2 = Post(title='Title2', slug='Sluggy',
                body='The body text.', author=u1.id)
      db.session.add(p2)
      db.session.commit()


   def tearDown(self):
      for table in reversed(db.metadata.sorted_tables):
         db.engine.execute(table.delete())
      db.session.commit()
      db.session.remove() 

   ########################
   #### Helper Methods ####
   ########################
   def register(self, username, email, fname, lname, password, confirm):
      return self.client.post(
         '/register',
         data = {
            'username': username,
            'email': email,
            'first': fname,
            'last': lname,
            'password': password,
            'password2': confirm
         },
         follow_redirects=True
      )
   
   def login(self, email, password):
      return self.client.post(
         '/login',
         data = {
            'email': email,
            'password': password
         },
         follow_redirects=True
      )

   def logout(self):
      return self.client.get('/logout', follow_redirects = True)

   #########################
   ####   Basic Tests   ####
   #########################

   def test_home_page_returns(self):
      resp = self.client.get('/')
      self.assertEqual(200, resp.status_code)

   def test_home_page_returns_correct_html(self):
      resp = self.client.get('/')
      html = resp.data.decode('utf-8')
      self.assertTrue(html.startswith('<!DOCTYPE html>'))
      self.assertIn('<title>Fancy-Pants Blog</title>', html)
      self.assertTrue(html.endswith('</html>'))

   def test_menu_text(self):
      resp = self.client.get('/')
      html = resp.data.decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')
      menu = [link.get_text() for link in soup.select('.menu-item')]
      self.assertListEqual(['About', 'CV', 'Blog', 'Login', 'Register'], menu)

   def test_menu_links(self):
      resp = self.client.get('/')
      html = resp.data.decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')
      menu = [link.get('href') for link in soup.select('.menu-item a')]
      self.assertListEqual(['/about', '/cv', '/blog', '/login', '/register'], menu)

   def test_heading_no_name(self):
      resp = self.client.get('/')
      html = resp.data.decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')
      head = soup.h1.get_text()
      self.assertEqual('Hello Stranger', head)

   def test_heading_name(self):
      self.login('author@example.com', 'password')
      resp = self.client.get('/')
      html = resp.data.decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')
      head = soup.h1.get_text()
      self.assertEqual('Hello Author', head)

   ################################
   ####   Registration tests   ####
   ################################

   def test_valid_registration(self):
      resp = self.register('tester', 'testy@testing.com', 
                           'Test', 'Tester', 'GoodPassword', 'GoodPassword')
      self.assertEqual(resp.status_code, 200)
      self.assertIn(b'Thanks for registering!', resp.data)

   def test_different_passwords(self):
      resp = self.register('tester2', 'testy2@testing.com',
                           'Test', 'Tester', 'GoodPassword', 'BadPassword')
      self.assertEqual(resp.status_code, 200)
      self.assertIn(b'Field must be equal to password.', resp.data)

   def test_duplicate_registrations(self):
      resp = self.register('author', 'author@example.com',
                           'Test', 'Tester', 'GoodPassword', 'GoodPassword')
      self.assertIn(b'User already exists.', resp.data)

   def test_login_success(self):
      resp = self.login('author@example.com', 'password')
      self.assertIn(b'You were successfully logged in', resp.data)
   
   def test_login_invalid_email(self):
      resp = self.login('user17@example.com', 'password')
      self.assertIn(b'Invalid Email.', resp.data)
   
   def test_login_invalid_password(self):
      resp = self.login('author@example.com', 'Paword')
      self.assertIn(b'Invalid Password.', resp.data)
   
   def test_logout(self):
      self.login('author@example.com', 'password')
      resp = self.logout()
      self.assertIn(b'You are logged out.', resp.data)

   ##########################
   ####    Blog Tests    ####
   ##########################

   def test_blog_not_logged_in(self):
      resp = self.client.post('/post', data=dict(title="bad", slug="bad", text="bad"), follow_redirects=True)
      self.assertIn(b'You must be logged in', resp.data)
   
   def test_blog_logged_in(self):
      self.login('author@example.com', 'password')
      data = {
         'post_title': 'Test Post',
         'slug': 'Short summary of the post.',
         'text': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer bibendum enim id enim tempor, ullamcorper tempor quam tincidunt. Proin eget dapibus arcu. Donec ornare feugiat elit, eu efficitur nisi dictum in. Donec libero nisl, pretium eget placerat nec, tincidunt varius orci. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc consequat leo enim, ut maximus neque pellentesque ac. Quisque porta, justo in maximus tincidunt, eros arcu tempus elit, a tristique turpis quam vel lacus. Nulla eleifend felis venenatis nunc ullamcorper cursus. Duis scelerisque consectetur odio, quis aliquet ipsum dictum vel. In dapibus, nisl ut feugiat vehicula, diam justo gravida lorem, id gravida nulla est id est. Donec ut nulla eu urna auctor gravida at eu purus. Etiam nulla dolor, tincidunt a nisl in, porta efficitur felis. Donec pretium lobortis facilisis. '''
      }
      resp = self.client.post('/post', data=data, follow_redirects=True)
      self.assertIn(b'Test Post', resp.data)

   def test_get_all_posts(self):
      self.login('author@example.com', 'Password')
      resp = self.client.get('/blog')
      self.assertIn(b'Title', resp.data)
      self.assertIn(b'Title2', resp.data)

   def test_get_one_post(self):
      resp = self.client.get('/blog/1')
      self.assertIn(b'Title', resp.data)
      self.assertNotIn(b'Title2', resp.data)

   

   
