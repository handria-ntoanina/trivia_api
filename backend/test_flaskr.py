import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from config import ConfigTest

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # This is already calling setup_db to the test DB
        self.app = create_app(test_config=ConfigTest())
        self.client = self.app.test_client
        self.db = self.app.db
        self.new_question = {'question': 'Does this test work?', 'answer': 'maybe',
                             'category': 'testing', 'difficulty': 4}

    def tearDown(self):
        """Executed after reach test"""
        pass

    def assert_404(self, res):
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(res.status_code, 404)

    def assert_422(self, res):
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(res.status_code, 422)

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
    
    def test_retrieve_categories_as_dict(self):
        Category.query.delete()
        cat = Category(type='temp')
        self.db.session.add(cat)
        self.db.session.commit()
        res = self.client().get('/api/categories')
        res = json.loads(res.data)
        categories = res['categories']
        for k in categories.keys():
            self.assertEqual(categories[k], 'temp')

    def test_retrieve_categories_error(self):
        # Try to get categories when the table is empty
        Category.query.delete()
        self.db.session.commit()
        res = self.client().get('/api/categories')
        self.assert_404(res)
    
    def test_retrieve_questions(self):
        size = QUESTIONS_PER_PAGE * 2
        self.generate_test_data(size)
        res = self.client().get('/api/questions')
        res = json.loads(res.data)
        self.assertTrue(res['success'])
        self.assertEqual(len(res['questions']), QUESTIONS_PER_PAGE)
        self.assertEqual(res['total_questions'], size)
        
    def test_retrieve_questions_includes_categories(self):
        # Build categories on empty DB
        Category.query.delete()
        cat = Category(type='temp')
        self.db.session.add(cat)
        self.db.session.commit()
        size = QUESTIONS_PER_PAGE * 2
        self.generate_test_data(size)
        res = self.client().get('/api/questions')
        res = json.loads(res.data)
        self.assertTrue('categories' in res)
        categories = res['categories']
        for k in categories.keys():
            self.assertEqual(categories[k], 'temp')
        
    def test_retrieve_questions_from_page(self):
        size = QUESTIONS_PER_PAGE * 2
        self.generate_test_data(size)
        res = self.client().get('/api/questions?page=2')
        res = json.loads(res.data)
        self.assertTrue(res['success'])
        self.assertEqual(res['questions'][0]['question'], 'question10')
        self.assertEqual(len(res['questions']), QUESTIONS_PER_PAGE)
        self.assertEqual(res['total_questions'], size)

    def generate_test_data(self, size):
        # Empty the table question and add some rows
        Question.query.delete()
        for i in range(size):
            s = str(i) if i >= 10 else '0' + str(i)
            question = Question('question' + s, 'answer' + s, 'category', i)
            self.db.session.add(question)
        self.db.session.commit()

    def test_retrieve_questions_error(self):
        res = self.client().get('/api/questions?page=100')
        self.assert_404(res)
    
    def test_delete_question(self):
        self.generate_test_data(2)
        res = self.client().get('/api/questions')
        res = json.loads(res.data)
        question = res['questions'][0]
        res = self.client().delete('/api/questions/{}'.format(question['id']))
        res = json.loads(res.data)
        self.assertTrue(res['success'])
        res = self.client().get('/api/questions')
        res = json.loads(res.data)
        self.assertTrue(res['success'])
        self.assertEqual(res['total_questions'], 1)
        self.assertTrue(question['id'] not in [q['id'] for q in res['questions']])
        
    def test_delete_question_error(self):
        Question.query.delete()
        self.db.session.commit()
        res = self.client().delete('/api/questions/1')
        self.assert_404(res)

    def test_create_question(self):
        Question.query.delete()
        self.db.session.commit()
        res = self.client().post('/api/questions', json=self.new_question)
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.data)
        self.assertTrue(res['success'])
        res = self.client().get('/api/questions')
        res = json.loads(res.data)
        self.assertEqual(res['total_questions'], 1)
        self.assertEqual(res['questions'][0]['question'], self.new_question['question'])
        self.assertEqual(res['questions'][0]['answer'], self.new_question['answer'])
        self.assertEqual(res['questions'][0]['category'], self.new_question['category'])
        self.assertEqual(res['questions'][0]['difficulty'], self.new_question['difficulty'])
        
    def test_create_question_error(self):
        res = self.client().post('/api/questions/45', json=self.new_question)
        self.assertEqual(res.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
