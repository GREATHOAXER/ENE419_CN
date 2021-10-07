import requests
import time
import csv
from time import gmtime, strftime
from telegram.ext import Updater
from apscheduler.schedulers.background import BackgroundScheduler
#Global variables
updater = Updater("2007419725:AAGmCJtaPECVdBwK8QjZSv3I2ALT66EfJbY")

def test():
    r = requests.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,KRW")
    line = r.json()
    f = open('test.csv','a',newline="\n")
    wf = csv.writer(f)
    coinList = [strftime("%Y-%m-%d-%H:%M:%S", time.localtime()),line["USD"],line["KRW"]]
    wf.writerow(coinList)
    f.close()
    try:
        updater.bot.send_message(chat_id=2037124410, text=coinList)
    except KeyboardInterrupt:
        updater.bot.send_message(chat_id=2037124410, text='Keyboard Interrupt!')
        exit(0)

    



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
        try:
            pass
        except KeyboardInterrupt:
            updater.bot.send_message(chat_id=2037124410, text='Keyboard Interrupt!')
            exit(0)