from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.Enum('male', 'female'))
    group = db.Column(db.Enum('A', 'B', 'C'))
    email = db.Column(db.String(100))

    birthday = db.Column(db.String(80), nullable=False)
    terms = db.Column(db.Boolean, nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))

    def __repr__(self):
        return f'Student({self.surname} {self.name} - group {self.group})'


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    students = db.relationship('Student', backref='faculty', lazy=True)

    def __repr__(self):
        return f'Faculty({self.name})'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    copies = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return f'Book({self.name})'


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f'Author({self.name} {self.surname})'


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    subject_name = db.Column(db.String(100))
    mark = db.Column(db.Integer)
    student = db.relationship('Student', backref='marks', lazy=True)
