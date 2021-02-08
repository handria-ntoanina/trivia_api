import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import func

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
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    def paginate(request, query):
        page = request.args.get('page', 1, type=int)
        # if 1st index of the page is greater than the last index of the result
        # then abort
        if query.count() - 1 < (page - 1) * QUESTIONS_PER_PAGE:
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
            'categories': {cat.id: cat.type for cat in selection},
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
        selection = Question.query
        search_term = request.args.get('searchTerm')
        if search_term:
            selection = selection.filter(Question.question.ilike('%{}%'.format(search_term)))
        return return_questions(selection)

    def return_questions(selection):
        selection = selection.order_by(Question.question)
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
    
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if not question:
            abort(404)
        try:
            app.db.session.delete(question)
            app.db.session.commit()
            return jsonify({
                'success': True
            })
        except:
            abort(422)
    
    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/api/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        
        new_question = body.get('question', None)
        new_category = body.get('category', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', 0)
        
        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            app.db.session.add(question)
            app.db.session.commit()
            return jsonify({
                    'success': True
                }), 200

        except:
            abort(422)
        
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    # Instead of a specific method to handle a POST, the method retrieve_questions for GET
    # has been updated to take into account filtering
    # A GET is more appropriate as it is about getting filtered questions
    
    '''
    @TODO:
    Create a GET endpoint to get questions based on category.
    
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/api/categories/<int:category_id>/questions')
    def retrieve_category_question(category_id):
        selection = Question.query.filter(Question.category == category_id)
        return return_questions(selection)
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

    @app.route('/api/quizzes', methods=['POST'])
    def generate_quiz():
        body = request.get_json()
    
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
 
        if not quiz_category:
            # check https://stackoverflow.com/questions/7939137/right-http-status-code-to-wrong-input
            abort(422)

        try:
            questions = Question.query.filter(Question.id.notin_(previous_questions))
            # 0 is for all category
            if quiz_category["id"] != 0:
                questions = questions.filter(Question.category == quiz_category["id"])
            
            # check https://stackoverflow.com/questions/60805/getting-random-row-through-sqlalchemy
            question = questions.order_by(func.random()).limit(1).one_or_none()
            if not question:
                return jsonify({
                    'success': True,
                    'question': None
                }), 200
            
            return jsonify({
                'success': True,
                'question': question.format()
            }), 200
            
        except:
            abort(422)
    
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
