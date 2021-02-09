# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# API Reference
* Base URL: At present, this app can be run locally and is not hosted as a base URL.The backend app is hosted at the default, 
http://127.0.0.1:5000/api, which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API keys. 
## Error handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:
* 400: Bad Request
* 404: Resource Not Found
* 422: Not Processable

## Endpoints
* GET /categories
* GET /categories/<int:category_id>/questions
* GET /questions
* DELETE /questions/<int:question_id>
* POST /questions
* POST /quizzes

## GET /categories
- Fetches a dictionary of categories in which which the keys are the ids and the value is the corresponding string 
of the category
- Request Arguments: None
- Returns: 
    - categories: dictionary of categories where keys are ids and the value is the corresponding string of the category
    - total_categories: indicating the number of categories
- Sample:
```bash
curl -X GET http://localhost:5000/api/categories
```
- Output Sample:
```bash
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "total_categories": 6
}
```
## GET /categories/<int:category_id>/questions
- Fetches the questions belonging to a given category. The results are paginated in
groups of 10. Pages can be accessed by supplying a request parameter 'page' to choose
page number starting from 1
- Request Arguments: 
    - category_id which is the id of the category to be supplied in the URL
    - page, a request param to choose page number starting from 1
- Returns:
    - questions: an array of question objects that belong to the given category
    - categories: a dictionary of all categories where keys are the ids and values, the corresponding string of the category
    - total_questions: number of questions belonging to the category
- Sample:
```bash
curl -X GET http://localhost:5000/api/categories/4/questions
```
- Output Sample:
```bash
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },...
    ],
    "success": true,
    "total_questions": 4
}
```
## GET /questions
- Fetches all questions. The results are paginated in
groups of 10. Pages can be accessed by supplying a request parameter 'page' to choose
page number starting from 1. The results can be filtered also by providing
a request parameter 'searchTerm'
- Request Arguments:
    - searchTerm, when provided, the questions that contain the searchTerm (case insensitive) will be returned. When 
    that parameter is empty, all questions will be returned
    - page, a request param to choose page number starting from 1
- Returns:
    - questions: when searchTerm is provided, this is an array of question objects that match searchTerm. Otherwise,
    this contains an array of all questions in form of object. In both case, this array is paginated so only one page 
    is fetched at anytime 
    - categories: a dictionary of all categories where keys are the ids and values, the corresponding string of the category
    - total_questions: number of questions matching searchTerm if searchTerm is provided, otherwise
    this is the number of all questions
- Sample:
```bash
curl -X GET 'http://localhost:5000/api/questions?page=1&searchTerm=Which'
```
- Output Sample:
```bash
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },...
    ],
    "success": true,
    "total_questions": 6
}
```

## POST /questions
- Adds a new question to the trivia database
- Request Arguments: These are expected to be a JSON in the request body
    - question: the question to be displayed to the user in form of interrogation
    - category: id of the category that will contain the question
    - answer: expected answer of the question
    - difficulty: indicates the level of difficulty of the question from 1 to 5
- Returns: None
- Sample:
```bash
curl -X POST \
  http://localhost:5000/api/questions \
  -H 'Content-Type: application/json' \
  -d '{
	"question":"Is this a sample question?",
	"answer":"I think so",
	"category":4,
	"difficulty":5
    }'
```
## DELETE /questions/<int:question_id>
- Deletes a question from the trivia database
- Request Arguments: question_id which is the id of the question to be deleted
- Returns: None
- Sample:
```bash
curl -X DELETE \
  http://localhost:5000/api/questions/24 \
```
## POST /quizzes
- After each call, fetches one random question to play the quiz. Previously returned question are not fetched again.
- Request Arguments: These are expected to be a JSON in the request body
    - previous_questions: an array of question ids that were already played and should not be asked again during the quizzes
    - quiz_category: object category with attributes type and id from which the questions 
    should be fetched from. If an id=0 is provided, then all questions of the trivia can be
    part of the quizzes 
- Returns: question as an object with attributes answer, category, difficulty, 
id, and the question itself
- Sample:
```bash
curl -X POST \
  http://localhost:5000/api/quizzes \
  -H 'Content-Type: application/json' \
  -d '{
	"previous_questions": [14],
	"quiz_category": {"id":3, "type": "Geography"}
}'
```
- Output Sample:
```bash
{
    "question": {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
    },
    "success": true
}
```