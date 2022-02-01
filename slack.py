import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def post_slack(msg):
  url = os.getenv('SLACK_MAIN_HOOK')
  headers = {'Content-type': 'application/json'}
  r = requests.post(url, data=json.dumps(msg), headers=headers)
  print(r.content)

def create_sections(topic, title, link, content):
  return (
    {
      "type": "section",
      "text": {
      "type": "mrkdwn",
        "text": f'｜{topic}｜'
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": f'_*:round_pushpin:{title}*_'
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": f'`網站連結`：{link}'
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": content
      }
    },
    {
      "type": "divider"
    },
  )


def fill_message(sections):
  return {
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": f'【程人日報:rolled_up_newspaper: {datetime.today().strftime("%Y/%m/%d %a.")}】'
        }
      },
      {
        "type": "context",
        "elements": [
          {
            "text": f'{datetime.today().strftime("%b %d, %Y ｜ %a.")}',
            "type": "mrkdwn"
          }
        ]
      },
      {
        "type": "divider"
      },
      *sections
    ]
  }

def send_err(err):
  url = os.getenv('SLACK_TEST_HOOK')
  headers = {'Content-type': 'application/json'}
  msg = {'text': err} if type(err) == str else err
  r = requests.post(url, data=json.dumps(msg), headers=headers)
  print(r.content)
  