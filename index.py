from flask import Flask, render_template, redirect, url_for, request
from main import get_post_page, get_post_msg
import slack as sl
import notion as no

app = Flask(__name__)

@app.route("/")
def index():
  PAGE_ID, name = get_post_page()
  return render_template('index.html', info=name, PAGE_ID=PAGE_ID)

@app.route("/post", methods=['POST'])
def post():
  PAGE_ID = request.args.get('id')
  if PAGE_ID != '':
    msg = get_post_msg(PAGE_ID)
    sl.post_slack(msg)
    no.update_status(PAGE_ID)
    no.create_page('c20f4fd6438f4c75aa3e06096b9c8b23')
  return redirect(url_for('index'))

@app.route("/test", methods=['POST'])
def test():
  PAGE_ID = request.args.get('id')
  if PAGE_ID != '':
    msg = get_post_msg(PAGE_ID)
    sl.send_err(msg)
  return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(debug=True)