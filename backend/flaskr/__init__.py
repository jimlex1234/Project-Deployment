
from json import load
import os
import string
from unicodedata import category
from unittest import result
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.orm import load_only

from sqlalchemy import select

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(page, questions_data):
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions_data]
    return questions[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        return response

    @app.get('/categories')
    def fetch_categories():
        categories = Category.query.order_by(Category.id).all()
        if not categories:
            abort(404)
        return jsonify({
            'categories': {category.id: category.type for category in categories}
        })
        

    @app.get('/questions')
    def fetch_questions():
        categories = Category.query.all()
        questions = Question.query.all()
        paginated_questions = paginate_questions(request.args.get("page", 1, type=int), questions)

        if not paginated_questions:
            abort(404)

        return jsonify({
                "questions": list(paginated_questions),
                "total_questions": len(questions),
                "current_category": '',
                "total_categories": {category.id: category.type for category in categories}
            })

    @app.delete('/questions/<int:id>')
    def remove_question(id):
        question = Question.query.get_or_404(id)            
        question.delete()
        questions = len(Question.query.all())
        return jsonify({
            'deleted': id,
            'total_questions': questions
        })
   
    @app.post('/questions')
    def post_question():
        body = request.get_json()
        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')

        if not question or not answer or not category or not difficulty:
            abort(422)

        try:
            question_db = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
                )
            db.session.add(question_db)
            db.session.commit()
            questions = Question.query.all()
            paginated_questions = paginate_questions(request.args.get("page", 1, type=int), questions)

            return jsonify({
            'created': question_db.id,
            'questions': paginated_questions,
            'total_questions': len(questions)
    })
        except:
            abort(422)

    @app.get('/questions/search')
    def search_questions():
        key = request.args.get('search')
        filtered_questions = Question.query.filter(Question.question.ilike(f'%{key}%')).all()
        paginated_questions = paginate_questions(request.args.get("page", 1, type=int), filtered_questions)

        if not key:
            abort(400)

        return jsonify({
                "questions": list(paginated_questions),
                "total_questions": len(filtered_questions),
            })

    @app.get('/categories/<string:category_id>/questions')
    def questions_by_category(category_id):
        try:
            filtered_questions = Question.query.filter(category_id == Question.category).all()
            paginated_questions = paginate_questions(request.args.get("page", 1, type=int), filtered_questions)
            category = Category.query.get(category_id)
            return jsonify({
                    "success": True,
                    "questions": list(paginated_questions),
                    "total_questions": len(filtered_questions),
                    "current_category": [category.type]
                })
        except:
            abort(404)
        

    @app.post('/quizzes')
    def play_quiz():
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            category_id = quiz_category['id']

            if category_id == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions), 
                Question.category == category_id).all()
            question = None
            if questions:
                question = random.choice(questions)

            return jsonify({
                'question': question.format()
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return( 
            jsonify({'error': 404,'message': 'The resource you are trying to access does not exist'}),
            404
        )
    
    @app.errorhandler(422)
    def unprocessed(error):
        return(
            jsonify({'error': 422,'message': 'Something went wrong :)'}),
            422

        )

    @app.errorhandler(400)
    def bad_request(error):
        return(
            jsonify({'error': 400,'message': 'Bad Request'}),
            400

        )

    @app.errorhandler(405)
    def not_allowed(error):
        return(
            jsonify({'error': 405,'message': 'This method is not allowed'}),
            405

        )
        
    return app

