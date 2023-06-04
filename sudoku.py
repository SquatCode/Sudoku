from flask import Flask, render_template

from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    name = None
    return render_template('index.html')