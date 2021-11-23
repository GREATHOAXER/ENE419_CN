import requests
import time
import csv
from time import gmtime, strftime
from telegram.ext import Updater, CommandHandler
from telegram import Update, Bot
from apscheduler.schedulers.background import BackgroundScheduler
    
def test():
    global previousPrice
    concurrency : str = "USD"
    concurrency2 : str = "KRW"
    coin: str = "BTC"
    r = requests.get("https://min-api.cryptocompare.com/data/price?fsym="+coin+"&tsyms="+concurrency+","+concurrency2)
    line = r.json()
    coinPriceInfo = [strftime("%Y-%m-%d-%H:%M:%S", time.localtime()),line[concurrency],line[concurrency2]]
    textLine : str = ""

    #File Part
    f = open('coinInfo.csv','a',newline="\n") #Append coin information in existing file
    wf = csv.writer(f)
    wf.writerow(coinPriceInfo)
    f.close()

    #price selection
    coinPrice = round(coinPriceInfo[1] - previousPrice, 3)
    if(coinPrice > 0 and previousPrice != 0):
        textLine: str = "Cryptocompare-"+coin+"-"+concurrency+": "+str(coinPriceInfo[1])+", UP " + str(coinPrice)
        
    elif(coinPrice < 0 and previousPrice != 0):
        textLine: str = "Cryptocompare-"+coin+"-"+concurrency+": "+str(coinPriceInfo[1])+", DOWN " + str((abs(coinPrice)))

    else:
        textLine: str = "Cryptocompare-"+coin+"-"+concurrency+": "+str(coinPriceInfo[1])

    #Send msg to telegram & update previous Price
    updater.bot.send_message(chat_id = chatId,text = textLine)
    previousPrice = coinPriceInfo[1]

def start(update, context):
    global previousPrice
    context.bot.send_message(chat_id=update.effective_chat.id, text="작업을 시작합니다.")
    sched.add_job(test,'interval',seconds = 5 ,id="test")
    previousPrice = 0
    print("작업 시작")
    

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="작업을 끝냅니다.")
    sched.remove_job('test')
    print("작업 끝")

#previous price initialization
previousPrice = 0

#Scheduler settings
sched = BackgroundScheduler()
sched.start()

#CSV file creation
f = open('coinInfo.csv','w')
fw = csv.writer(f)
fw.writerow(["Date", "BTC-USD", "BTC-KRW"])
f.close()

botToken = "2007419725:AAGmCJtaPECVdBwK8QjZSv3I2ALT66EfJbY"
chatId = 2037124410
updater = Updater(botToken, use_context= True)

dispatcher = updater.dispatcher
start_handler = CommandHandler('start',start)
end_handler = CommandHandler('stop',stop)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(end_handler)
    
updater.start_polling()
updater.idle()





