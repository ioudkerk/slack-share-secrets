import json
import requests
import uuid
import redis

from flask import Flask, jsonify, request, make_response
from slackeventsapi import SlackEventAdapter
from slack import WebClient

from cryptography.fernet import Fernet

from interactive_actions import route
from utils.secrets import gen_one_time_url
from utils import validators
from utils.parsers import parse_text
from config import SLACK_SIGNING_SECRET, \
    SLACK_BOT_TOKEN, \
    B_SLACK_SIGNING_SECRET        


app = Flask(__name__)

slack_client = WebClient(SLACK_BOT_TOKEN)

slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

@app.route("/slack/sharesecret", methods= ["POST"])
def slack_sharesecret():
    validators.verify(request, B_SLACK_SIGNING_SECRET)    
    parsed_msg = parse_text(request.form['text'])
    to_user = parsed_msg[0]
    msg = parsed_msg[1]    
    one_time_url = gen_one_time_url(msg)
    blocks = json.loads(open('templates/open_modal.json').read())
    blocks['blocks'][1]['elements'][0]['value'] += one_time_url
    slack_client.chat_postMessage(channel=to_user, blocks=blocks['blocks'])        
    return make_response("",200)

@app.route("/slack/interactive", methods= ["POST"])
def slack_interactive():
    validators.verify(request, B_SLACK_SIGNING_SECRET)
    payload = json.loads(request.form['payload'])    
    if payload['type'] == 'block_actions':
        return route.block_actions(payload)
    return make_response("",200)

@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

if __name__ == "__main__":
    app.run(port=3000)
