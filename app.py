from flask import Flask, jsonify, abort, request
import os

print(os.environ['API_KEY'])

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello"


app.run()
