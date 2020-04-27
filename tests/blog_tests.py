import unittest
from app import app

class TestBlog(unittest.TestCase):

   def setUp(self):
      self.client = app.test_client()
   
   def test_hello_flask(self):
      resp = self.client.get('/')
      self.assertEqual(b'Hello Flask!', resp.data)