from datetime import datetime

# import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

app = Flask(__name__)

# define the job
@app.route('/')
def hello_job():
    print('Hello Job! The time is: %s' % datetime.now())



    # init BackgroundScheduler job
scheduler = BackgroundScheduler()
    # in your case you could change seconds to hours
scheduler.add_job(hello_job, trigger='interval', seconds=3)
scheduler.start()
