from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return f"Привет Мир!!!"


if __name__ == "__main__":
    app.run(debug=True)
