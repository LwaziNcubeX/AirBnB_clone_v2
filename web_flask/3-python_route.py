#!/usr/bin/python3
"""A script that starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """return hello HBNB message"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """return ..... HBNB message"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def display_c(text):
    """display text after C Character"""
    input_text = text.replace('_', ' ')

    return f'C {input_text}'


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python(text='is cool'):
    """display text after python Character"""
    input_text = text.replace('_', ' ')

    return f'Python {input_text}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
