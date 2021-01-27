import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from config import ConfigTest

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # This is already calling setup_db to the test DB
        self.app = create_app(test_config=ConfigTest())
        self.client = self.app.test_client
        self.db = self.app.db

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_retrieve_categories(self):
        # Build categories on empty DB
        Category.query.delete()
        cat = Category(type='temp')
        self.db.session.add(cat)
        self.db.session.commit()
        res = self.client().get('/api/categories')
        res = json.loads(res.data)
        self.assertTrue(res['success'])
        self.assertTrue(len(res['categories']) > 0)
        self.assertTrue(res['total_categories'] > 0)

    def test_retrieve_categories_error(self):
        # Try to get categories when the table is empty
        Category.query.delete()
        self.db.session.commit()
        res = self.client().get('/api/categories')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()