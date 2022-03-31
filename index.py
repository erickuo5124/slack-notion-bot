from flask import Flask, render_template, redirect, url_for, request
from main import get_post_page, get_post_msg
import slack as sl
import notion as no
import discord as dc

app = Flask(__name__)

@app.route("/")
def index():
  PAGE_ID, name = get_post_page()
  sl_msg = ''
  if PAGE_ID != '':
    sl_msg, _ = get_post_msg(PAGE_ID)
  return render_template('index.html', info=name, PAGE_ID=PAGE_ID, preview_msg=sl_msg)

@app.route("/post", methods=['POST'])
def post():
  PAGE_ID = request.args.get('id')
  if PAGE_ID != '':
    msg, dc_msg = get_post_msg(PAGE_ID)
    # sl.post_slack(msg)
    no.update_status(PAGE_ID)
    # no.create_page('c20f4fd6438f4c75aa3e06096b9c8b23')
    dc.post_discord(dc_msg)
  return redirect(url_for('index'))

@app.route("/test", methods=['POST'])
def test():
  PAGE_ID = request.args.get('id')
  if PAGE_ID != '':
    msg, _ = get_post_msg(PAGE_ID)
    sl.send_err(msg)
  return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(debug=True)