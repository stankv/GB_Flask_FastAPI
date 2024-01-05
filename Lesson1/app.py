from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/shop/')
def shop():
    return render_template('shop.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/jackets/')
def jackets():
    _jackets = [
        {
            "gender": "М",
            "season": "осень",
            "style": "классик",
            "size": 50,
            "brand": "Brand1",
            "view": "Фото"
        },
        {
            "gender": "М",
            "season": "зима",
            "style": "унисекс",
            "size": 52,
            "brand": "Brand2"
        },
        {
            "gender": "Ж",
            "season": "лето",
            "style": "классик",
            "size": 42,
            "brand": "Brand3"
        },
    ]
    context = {"jackets": _jackets}
    return render_template('jackets.html', **context)


@app.route('/jacket/')
def jacket():
    return render_template('jacket.html')


if __name__ == '__main__':
    app.run(debug=True)