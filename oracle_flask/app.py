import cx_Oracle
import time
import numpy as np
import pandas as pd
import sqlalchemy #pip install sqlalchemy, pip install psycopg2-binary
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

# flask
app = Flask(__name__)
# oracle database connection
cx_Oracle.init_oracle_client(lib_dir=r'C:/projects/market_pred/instantclient_21_6')
engine = sqlalchemy.create_engine('oracle+cx_oracle://USERNAME:PASSWORD@DATABASE_NAME')

my_2darray = np.array([[1, 2, 3], [4, 5, 6]])
df = pd.DataFrame(my_2darray)

#scheduler test function
def time_counter():
    #get latest date from database
    for i in range(10):
        print('counter:',i)
        time.sleep(1)

    # if you want put or get data from oracle database, use the code below.
    # df = df.to_sql(name='TABLE_NAME', con=engine, if_exists='append') #if_exist='append' or 'replace'
    # df = pd.read_sql('SELECT * FROM YOUR_TABLE', con=engine)

@app.route('/')
def push_data():
    return 'HELLO!'

if __name__ == '__main__':
    scheduler = BackgroundScheduler(timezone="Asia/Seoul")
    # time interval scheduler
    scheduler.add_job(time_counter, 'interval', seconds=15)
    # periodical scheduler
    # scheduler.add_job(time_counter, 'cron', day_of_week='mon-sat', hour=9, minute=30, id="get_data")
    scheduler.start()
    # for all ip: host='0.0.0.0', for local ip: host='127.0.0.1'
    app.run(host='0.0.0.0', port=5000, debug=True)
