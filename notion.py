import requests
import json
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_TOKEN = os.getenv('NOTION_SECRET_TOKEN')
NOTION_API = os.getenv('NOTION_API')

def get_database(
  DATABASE_ID,
  sorts= [
    {
      'timestamp': 'created_time',
      "direction": "descending"
    }
  ],
  filter={
    'or': []
  }
):
  if DATABASE_ID == '': return []
  headers = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {SECRET_TOKEN}',
    'Notion-Version': '2021-08-16'
  }
  datas = {
    'sorts': sorts,
    'filter': filter
  }
  URL = f'{NOTION_API}/databases/{DATABASE_ID}/query'
  res = requests.post(URL, data=json.dumps(datas), headers=headers)
  return res.json()

def get_children(BLOCK_ID):
  if BLOCK_ID == '': return []
  headers = {
    'Authorization': f'Bearer {SECRET_TOKEN}',
    'Notion-Version': '2021-08-16',
  }
  URL = f'{NOTION_API}/blocks/{BLOCK_ID}/children'
  res = requests.get(URL, headers=headers)
  return res.json()

def update_status(PAGE_ID):
  headers = {
    'Authorization': f'Bearer {SECRET_TOKEN}',
    'Notion-Version': '2021-08-16',
    'Content-type': 'application/json',
  }
  datas = {
    "properties": {
      "Status": { 
        "select": { 'id': '7546a642-004c-464e-b258-a4e117dffe63' } 
      }
    }
  }
  URL = f'{NOTION_API}/pages/{PAGE_ID}'
  requests.patch(URL, data=json.dumps(datas), headers=headers)

def create_page(DATABASE_ID):
  if DATABASE_ID == '': return []
  headers = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {SECRET_TOKEN}',
    'Notion-Version': '2021-08-16'
  }
  template = open('page_template.json')
  datas = json.load(template)
  datas['parent']['database_id'] = DATABASE_ID
  tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
  datas['properties']['Title']['title'][0]['text']['content'] = f'程人日報 #{tomorrow.month}/{tomorrow.day}'
  URL = f'{NOTION_API}/pages'
  requests.post(URL, data=json.dumps(datas), headers=headers)

def print_json(txt):
  pretty = json.dumps(txt, indent=2, ensure_ascii=False)
  print(pretty)
  