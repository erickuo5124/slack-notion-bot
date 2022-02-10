import sys
import os
from dotenv import load_dotenv
import notion as no
import slack as sl

load_dotenv()
DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

def get_post_page():
  try:
    database = no.get_database(
      DATABASE_ID, 
      filter={
        "property": "Status",
        "select": { "equals": '待發布' }
      }
    )
    pages = database['results']
    PAGE_ID = pages[0]['id']
    PAGE_NAME = pages[0]['properties']['Title']['title'][0]['text']['content']
    return PAGE_ID, PAGE_NAME
  except:
    error = '尚未完成新聞稿或尚未開啟新的新聞稿頁面'
    return '', error

def get_post_msg(PAGE_ID):
  children = no.get_children(PAGE_ID)
  sections = []
  error = ''
  for block in children['results']:
    if 'child_database' not in block : break
    topic = block['child_database']['title']
    block_id = block['id']
    db = no.get_database(block_id)['results'][0]['properties']
    try:
      title = db['Title']['title'][0]['text']['content']
      link = db['Link']['rich_text'][0]['text']['content']
      content = db['Content']['rich_text'][0]['text']['content']
      sec = sl.create_sections(topic, title, link, content)
      sections.extend([*sec])
    except:
      error = '有人沒寫日報！'
      sl.send_err(error)
      sys.exit(1)
  msg = sl.fill_message(sections[:-1])
  return msg

if __name__ == '__main__':
  PAGE_ID, name = get_post_page()
  if PAGE_ID != '' and len(sys.argv) < 2:
    msg = get_post_msg(PAGE_ID)
    sl.post_slack(msg)
    no.update_status(PAGE_ID)
    no.create_page('c20f4fd6438f4c75aa3e06096b9c8b23')
  elif PAGE_ID != '' and sys.argv[1] == 'test':
    msg = get_post_msg(PAGE_ID)
    sl.send_err(msg)
  else:
    sys.exit(1)
  sys.exit(0)
