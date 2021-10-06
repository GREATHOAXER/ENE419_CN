import requests
import time
import csv
from time import gmtime, strftime
from apscheduler.schedulers.background import BackgroundScheduler

def test():
    r = requests.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,KRW")
    line = r.json()
    f = open('test.csv','a',newline="\n")
    wf = csv.writer(f)
    wf.writerow([strftime("%Y-%m-%d-%H:%M:%S", time.localtime()),line["USD"],line["KRW"]])
    f.close()

    



if __name__ == '__main__':
    sched = BackgroundScheduler()
    sched.start()
    f = open('test.csv','w')
    wf = csv.writer(f)
    wf.writerow(["Date", "BTC-USD", "BTC-KRW"])
    f.close()
    #execute test every 5 seconds
    sched.add_job(test,'interval',seconds = 5,id="test")
    
    while True:
        time.sleep(1.5)