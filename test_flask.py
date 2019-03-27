from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    j = jsonify({'key': None})

    return j

if __name__ == '__main__':
    app.run()