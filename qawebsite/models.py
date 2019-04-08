from datetime import datetime
from qawebsite import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False, unique=True)
    questions = db.relationship('Question', backref='user', lazy=True)
    answers = db.relationship('Answer', backref='user', lazy=True)
    forums = db.relationship('Forum', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.full_name}')"


class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    questions = db.relationship('Question', backref='forum', lazy=True)
    answers = db.relationship('Answer', backref='forum', lazy=True)

    def __repr__(self):
        return f"Forum('{self.id}', '{self.start_date}', '{self.end_date}')"

    def serialize(self):
        return {
            'id': self.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'user': self.user.full_name,
            'questions': [str(q) for q in self.questions],
            'answers': [str(a) for a in self.answers]
        }


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    qa_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)

    def __repr__(self):
        return f"Question('{self.date_posted}', '{self.text}')"


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text)
    image_url = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    qa_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)

    def __repr__(self):
        return f"Answer('{self.date_posted}', '{self.text}', '{self.image_url}', '{self.user}')"

