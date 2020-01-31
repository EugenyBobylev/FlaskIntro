from flask import Flask
from flask import render_template, flash, redirect
from config import Config
from app.forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Эльдар Рязанов'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'какая гадость ваша заливная рыба...'
        }
    ]
    return render_template('index.html', title='О кино', user=user, posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for ustr {form.username.data}, remember_me = {form.remember_me.data}')
        return redirect('/index')
    return render_template('login.html', title='Sign in', form=form)


@app.route('/user/<name>')
def hello(name):
    return name


if __name__ == "__main__":
    app.run(debug=True)
