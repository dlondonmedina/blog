import unittest
import requests

class TestBlog(unittest.TestCase):

   def setUp(self):
      self.url = 'http://127.0.0.1:5000/'

   def test_hello_flask(self):
      resp = requests.get(self.url)
      self.assertIn('Hello Flask!', resp.text)
   