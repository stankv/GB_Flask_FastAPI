from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    group = db.Column(db.Enum('A', 'B', 'C'))
    email = db.Column(db.String(100))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))

    def __repr__(self):
        return f'Student({self.surname} {self.name} - group {self.group})'


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    students = db.relationship('Student', backref='faculty', lazy=True)

    def __repr__(self):
        return f'Faculty({self.name})'
