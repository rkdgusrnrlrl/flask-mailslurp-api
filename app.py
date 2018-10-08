from flask import Flask, jsonify, abort, request
import os
from mailslurp_client import MailSlurpClient
from flask_cors import CORS

mail_api = MailSlurpClient(os.environ['API_KEY'])

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Hello"


@app.route("/inboxes", methods=['GET'])
def inboxes():
    return jsonify(mail_api.get_inboxes())


@app.route("/inboxes/<inbox_id>/messages", methods=['GET'])
def message(inbox_id):
    messages = mail_api.get_messages(inbox_id)
    for msg in messages:
        m = mail_api.get_eamil_text_contents(msg['body'])
        if m is not None:
            msg['contents'] = m
        else:
            msg['contents'] = ''
        msg.pop('body', None)

    return jsonify(messages)


app.run()
