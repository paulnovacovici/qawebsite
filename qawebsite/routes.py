from flask import request, jsonify
from qawebsite.models import User, Question, Forum, Answer
from qawebsite import app
from qawebsite import db
from datetime import datetime


@app.route('/')
def hello():
    return "Hello World"


@app.route('/qa', methods=['POST'])
def create_qa_session():
    content = request.get_json()
    # If key doesn't exist flask will throw a HTTP 400 Bad Request
    user_name = content['host_name']
    start_date = content['start_time']
    end_date = content['end_time']

    # @TODO: Should do checking of date to see if it is correct format
    # If data is incorrect format it throws 500 error
    month, day, year = start_date.split('/')
    start_dt = datetime(int(year), int(month), int(day))

    month, day, year = end_date.split('/')
    end_dt = datetime(int(year), int(month), int(day))

    user = User.query.filter_by(full_name=user_name).first()
    if not user:
        # Create a User
        user = User(full_name=user_name)
        db.session.add(user)
        db.session.commit()

    forum = Forum(start_date=start_dt, end_date=end_dt, user_id=user.id)
    db.session.add(forum)
    db.session.commit()

    return jsonify(dict(qa_id=forum.id))


@app.route('/qa/<int:qa_id>', methods=['GET'])
def retrieve_qa_session(qa_id):
    forum = Forum.query.filter_by(id=qa_id).first()

    if forum:
        return jsonify(forum.serialize())
    else:
        return 'No qa session found', 400


@app.route('/question/<int:qa_id>', methods=['POST'])
def ask_question(qa_id):
    content = request.get_json()
    question = content['text']
    full_name = content['asked_by_name']

    user = User.query.filter_by(full_name=full_name).first()
    if not user:
        # Create a User
        user = User(full_name=full_name)
        db.session.add(user)
        db.session.commit()

    forum = Forum.query.filter_by(id=qa_id).first()
    if not forum:
        return 'No qa session found', 400

    question = Question(text=question, user_id=user.id, qa_id=qa_id)
    db.session.add(question)
    db.session.commit()

    return jsonify(dict(question_id=question.id, question=question.text))


@app.route('/answer/<int:question_id>', methods=['POST'])
def answer_question(question_id):
    content = request.get_json()
    question_id = content['question_id']
    answer = content['text']
    image_url = content['image_url']
    user_name = content['answered_by']

    user = User.query.filter_by(full_name=user_name).first()
    if not user:
        # Create a User
        user = User(full_name=user_name)
        db.session.add(user)
        db.session.commit()

    question = Question.query.filter_by(id=question_id).first()
    if not question:
        return "Bad question id", 400

    answer = Answer(text=answer, image_url=image_url, user_id=user.id, qa_id=question.qa_id)
    db.session.add(answer)
    db.session.commit()

    return jsonify(dict(status="OK"))


@app.route('/qa/<int:qa_id>/questions', methods=['GET'])
def retrieve_questions(qa_id):
    forum = Forum.query.filter_by(id=qa_id).first()

    if forum:
        return jsonify([str(q) for q in forum.questions])
    else:
        return 'No qa session found', 400
