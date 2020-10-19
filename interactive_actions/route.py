import json
from slack import WebClient
from config import SLACK_BOT_TOKEN
from flask import make_response

from utils.secrets import getsecret

slack_client = WebClient(SLACK_BOT_TOKEN)


def block_actions(payload):
    trigger_id = payload['trigger_id']
    actions = payload['actions']
    if len(actions) != 1:
        make_response("error",400)
    if 'value' not in actions[0]:
        return make_response("", 200)
    if 'secretsharing' in actions[0]['value']:
        secret_uuid = actions[0]['value'].split('_')[1]
        modal = json.loads(open('templates/share_secret.json').read())
        modal['blocks'][2]['text']['text'] = getsecret(secret_uuid)
        slack_client.views_open(trigger_id=trigger_id,view=modal)
        return make_response("", 200)