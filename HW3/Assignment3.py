import websockets
import asyncio 
import json

#globl file to save the orderbook data
orderFile = open("./order.txt","w")

async def upbit_client():
    async with websockets.connect("wss://api.upbit.com/websocket/v1") as websocket:
        #referred Upbit API [https://docs.upbit.com/docs/upbit-quotation-websocket]
        #request format -> json format
        request_format = [ 
             {"ticket":"UNIQUE-TICKET"},
             {
                 "type": "trade",
                 "codes":["KRW-BTC"],
             },
             {
                 "type": "orderbook",
                 "codes":["KRW-BTC"],
             }
        ]
        #convert dict to json
        data = json.dumps(request_format)

        #send request to Upbit Server
        await websocket.send(data)
        
        while True:
                #Receive json data from Upbit Server via WebSocket
                data = await websocket.recv()
                #Convert json data to python dict
                data = json.loads(data)

                #Case 1. when received data is orderbook
                if(data['type'] == "orderbook"):
                    printList = []
                    #get first orderbook_units from orderbook
                    newData = data["orderbook_units"][0]
                    for info in newData:
                        line = str(info+": "+str(newData[info]))
                        printList.append(line)
                    print(", ".join(printList))
                    #Write data to text file
                    orderFile.write(", ".join(printList)+"\n")
                
                #Case 2. wheb received data is trade
                elif(data['type'] == "trade"):
                    printList = []
                    newData = data
                    #get trade_price/trade_volume/ask_bid from received data
                    tradeInfo = ["trade_price", "trade_volume", "ask_bid"]
                    for info in tradeInfo:
                        line = str(info+": "+str(newData[info]))
                        printList.append(line)
                    print(", ".join(printList))

async def main():
    await upbit_client()
    
 
if __name__ == "__main__":
    try:
        #asyncio -> for using asynchronous communication
        asyncio.run(main())
    #Keyboard Interrupt handling
    except KeyboardInterrupt:
        print("Keyboard Interrupt occured.")
        orderFile.close()
        exit()