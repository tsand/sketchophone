import os
from flask import Flask, render_template

app = Flask(__name__)

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# Templates (testing purposes)
@app.route('/base')
def base():
    return render_template('base.html')

# Pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sketch')
def sketch():
    return render_template('sketch.html')


if __name__ == '__main__':
    app.run(debug=True)