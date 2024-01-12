# Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
# содержать следующие поля:
# - Имя пользователя (обязательное поле)
# - Электронная почта (обязательное поле, с валидацией на корректность ввода email)
# - Пароль (обязательное поле, с валидацией на минимальную длину пароля)
# - Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
# После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
# и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
# заполнено или данные не прошли валидацию, то должно выводиться соответствующее
# сообщение об ошибке.
# Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
#базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
# об ошибке.


from flask import Flask, render_template, url_for, request
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from forms import LoginForm
from models import db, Student, Book, Mark

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seminar3.db'
db.init_app(app)
migrate = Migrate(app, db)

app.config[
    'SECRET_KEY'] = b'b0ee5a2c6515091072087d57c6693be951cd9fc4629e5e66324c8c33331b5768'
csrf = CSRFProtect(app)


@app.context_processor
def menu_items():
    menu_items = [
        {'name': 'Home', 'url': url_for("index")},
        {'name': 'Task 1', 'url': url_for("task_1")},
        {'name': 'Task 2', 'url': url_for("task_2")},
        {'name': 'Task 3', 'url': url_for("task_3")},
        {'name': 'LogIn', 'url': url_for("login")},
    ]
    return dict(menu_items=menu_items)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task_1')
def task_1():
    all_students = Student.query.order_by(-Student.id).all()
    return render_template('task_1.html', students=all_students)


@app.route('/task_2')
def task_2():
    all_books = Book.query.all()
    return render_template('task_2.html', all_books=all_books)


@app.route('/task_3')
def task_3():
    students = Student.query.all()  # Получаем всех студентов
    student_data = []

    for student in students:
        marks = Mark.query.filter_by(
            student_id=student.id).all()  # Получаем оценки для каждого студента
        mark_data = [{'subject_name': mark.subject_name, 'mark': mark.mark} for
                     mark in marks]
        student_info = {
            'id': student.id,
            'name': student.name,
            'surname': student.surname,
            'age': student.age,
            'gender': student.gender,
            'group': student.group,
            'email': student.email,
            'marks': mark_data
        }
        student_data.append(student_info)

    return render_template('task_3.html', students=student_data)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data
    email = form.email.data
    password = form.password.data
    context = {}
    if request.method == 'POST' and form.validate():
        if Student.query.filter(
                Student.username == username).all() or \
                Student.query.filter(Student.email == email).all():
            context = {'alert_message': "Пользователь уже существует!"}
            return render_template('login.html', form=form, **context)
        else:

            new_user = Student(username=username, email=email,
                               password=password)
            db.session.add(new_user)
            db.session.commit()
            context = {'alert_message': "Пользователь добавлен!"}
    return render_template('login.html', form=form, **context)
