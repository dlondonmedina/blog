import os 
import tempfile
from bs4 import BeautifulSoup
import unittest
from app import app
from app.models import Entry

class TestBlog(unittest.TestCase):

   def setUp(self):
      self.client = app.test_client()

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
      self.assertListEqual(['About', 'CV', 'Blog'], menu)

   def test_menu_links(self):
      resp = self.client.get('/')
      html = resp.data.decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')
      menu = [link.get('href') for link in soup.select('.menu-item a')]
      self.assertListEqual(['about', 'cv', 'blog'], menu)

   def test_heading_no_name(self):
      resp = self.client.get('/')
      html = resp.data.decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')
      head = soup.h1.get_text()
      self.assertEqual('Hello Stranger', head)

   def test_heading_name(self):
      resp = self.client.get('/Dylan')
      html = resp.data.decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')
      head = soup.h1.get_text()
      self.assertEqual('Hello Dylan', head)

   def test_form(self):
      resp = self.client.get('/post')
      html = resp.data.decode('utf-8')
      self.assertIn('<form method="POST">', html)
      self.assertIn('</form>', html)

   def test_form_fields(self):
      resp = self.client.get('/post')
      html = resp.data.decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')
      fields = [i.attrs['name'] for i in soup.find_all('input')]
      self.assertListEqual(fields[1:], ['post_title', 'author', 'submit'])
      self.assertEqual(soup.textarea.attrs['name'], 'text')
   

   
