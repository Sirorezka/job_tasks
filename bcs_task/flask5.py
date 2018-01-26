from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO, emit

## https://flask-socketio.readthedocs.io/en/latest/
## https://stackoverflow.com/questions/18395976/how-to-display-a-json-array-in-table-format

##
## https://flask-socketio.readthedocs.io/en/latest/

from random import random
import pandas as pd

app = Flask(__name__)
socketio = SocketIO(app)

#defines the job
def job():
    price_db = []
    new_price = random() 
    row1 = [new_price,new_price,new_price,new_price,new_price]
    new_price = random() 
    row2 = [new_price,new_price,new_price,new_price,new_price]
    price_db.append(row1)
    price_db.append(row2)
    price_db = pd.DataFrame(price_db)
    print (price_db)
    #job emits on websocket
    socketio.emit('price update',price_db.transpose().to_json(), broadcast=True)

def job3sec():
	print ("job 3 sec done")


def job7sec():
	print ("job 7 sec done")
	
	
#schedule job
scheduler = BackgroundScheduler()
running_job = scheduler.add_job(job, 'interval', seconds=4, max_instances=1)
running_job = scheduler.add_job(job3sec, 'interval', seconds=3, max_instances=1)
running_job = scheduler.add_job(job7sec, 'interval', seconds=7, max_instances=1)

scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
	
