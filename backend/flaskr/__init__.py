import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from config import Config

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config())
    else:
        # load the test config if passed in
        app.config.from_object(test_config)
    
    app.db = setup_db(app)
    
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    # CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,PUT,DELETE,OPTIONS')
        return response

    def paginate(request, query):
        page = request.args.get('page', 1, type=int)
        if query.count() < page * QUESTIONS_PER_PAGE:
            abort(404)
        selection = query.limit(QUESTIONS_PER_PAGE).offset((page - 1) * QUESTIONS_PER_PAGE).all()
        selection = [o.format() for o in selection]
        return selection
    
    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route("/api/categories")
    def retrieve_categories():
        selection = Category.query.order_by(Category.type).all()
        
        if len(selection) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': [cat.format() for cat in selection],
            'total_categories': len(selection)
        })
    
    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    
    @app.route('/api/questions')
    def retrieve_questions():
        selection = Question.query.order_by(Question.question)
        paginated = paginate(request, selection)
        return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': selection.count(),
                'categories': {cat.id: cat.type for cat in Category.query.order_by(Category.type).all()}
            })
    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    
    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    
    '''
    @TODO:
    Create a GET endpoint to get questions based on category.
    
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    
    
    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    
    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    
    return app
