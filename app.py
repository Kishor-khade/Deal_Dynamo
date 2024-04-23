from flask import Flask, render_template
import pandas as pd
import os
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import atexit
from collections import OrderedDict

def run_scripts():
    subprocess.call(['python', 'update.py'])
    subprocess.call(['python', 'ML.py'])

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.add_job(func=run_scripts, trigger='interval', hours=1)
scheduler.start()

atexit.register(lambda:scheduler.shutdown())

@app.route('/')
def index():
    df = pd.read_csv(os.path.join(os.getcwd(),'categorized_data.csv'))
    grouped_data = df.groupby('label')
    # Convert grouped data to a dictionary for easy rendering in the template
    categorized_data = {category: data.to_dict(orient='records') for category, data in grouped_data}
    categorized_data = OrderedDict(sorted(categorized_data.items(), key=lambda x:x[0], reverse=True))
    return render_template('aa.html', categorized_data=categorized_data)


if __name__=='__main__':
    app.run(debug=True)
