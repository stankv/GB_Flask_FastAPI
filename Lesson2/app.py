# Создать страницу, на которой будет форма для ввода имени и электронной почты.
# При отправке которой будет создан cookie файл с данными пользователя.
# Также будет произведено перенаправление на страницу приветствия, где 
# будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка "Выйти". При нажатии на кнопку 
# будет удален cookie файл с данными пользователя и произведено перенаправление
#  на страницу ввода имени и электронной почты.


from flask import Flask, render_template, redirect, url_for, request, make_response

app = Flask(__name__)


@app.route('/hello/<name>')
def hello(name):
    context = {"name": name}
    return render_template('hello.html', **context)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        login = request.form.get('login')
        email = request.form.get('email')
        # Создаем ответ и перенаправляем на страницу с приветствием
        response = make_response(redirect(url_for('hello', name=login)))
        # Создаем cookie
        response.set_cookie('login', login)
        response.set_cookie('email', email)
        return response
    return render_template('index.html')


@app.route('/getcookie')
def get_cookie():
    login = request.cookies.get('login')
    email = request.cookies.get('email')
    return f'Cookie - Имя: {login}, E-mail: {email}'


@app.route('/logout', methods=['POST'])
def logout():
    # Создаем ответ и перенаправляем на страницу входа
    response = make_response(redirect(url_for('index')))
    # Удаляем cookie
    response.delete_cookie('login')
    response.delete_cookie('email')
    return response


if __name__ == '__main__':
    app.run(debug=True)