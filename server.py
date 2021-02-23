from flask import Flask, render_template
from flask import request as flask_request
from flask import request
from controller import Controller
import logging
import logging.handlers
import time
from visited_db import VisitedDB
import json

logging.basicConfig(level=logging.INFO)
filehandler=logging.handlers.TimedRotatingFileHandler("./log/logger.log",'D',1,30)
filehandler.suffix="%Y%m%d-%H%M%S.log"
logging.getLogger('').addHandler(filehandler)

app = Flask(__name__)
app.debug=True
# app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)

@app.route('/')
def main():
    v_db = VisitedDB()
    ip = request.remote_addr
    c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    # print(c_time,ip)
    v_db.addItem(c_time,ip)
    # logging.info('{} : visiter ip-{}'.format(c_time,ip))
    return render_template('index.html')

@app.route('/getItemList')
def getItemList():
    url = flask_request.values['url']
    contr = Controller(url)
    items = contr.getInfo()
    # print(items)
    return json.dumps(items)
    # render_template('main.html',items=items)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)