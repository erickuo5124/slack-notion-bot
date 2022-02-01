import sys
import os
from dotenv import load_dotenv
import notion as no
import slack as sl

load_dotenv()
DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
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
  children = no.get_children(PAGE_ID)
except:
  error = '尚未完成新聞稿或尚未開啟新的新聞稿頁面'
  sl.send_err(error)
  sys.exit(1)

sections = []
error = ''
for block in children['results']:
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

if error == '' and len(sys.argv) < 2:
  sl.post_slack(msg)
  no.update_status(PAGE_ID)
  no.create_page(DATABASE_ID)
  sys.exit(0)
elif sys.argv[1] == 'test':
  sl.send_err(msg)
  sys.exit(0)

sys.exit(1)
