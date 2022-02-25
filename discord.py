import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def post_discord(msg):
  url = os.getenv('DISCORD_HOOK')
  headers = {'Content-type': 'application/x-www-form-urlencoded'}
  data = {"content": msg}
  r = requests.post(url, json=data)
  print(r.content)

def create_sections(topic, title, link, content):
  return f'｜{topic}｜\n\
:round_pushpin: ***{title}***\n\
`網站連結`：{link}\n\
{content}\n'


def fill_message(sections):
  content = f' **【程人日報:rolled_up_newspaper: {datetime.today().strftime("%Y/%m/%d %a.")}】**\n\
`{datetime.today().strftime("%b %d, %Y")}｜ by 程人日報小編`\n'
  for sec in sections:
    content += '\n'
    content += sec
  content += '\n'
  return content

if __name__ == '__main__':
  post_discord('hi')

