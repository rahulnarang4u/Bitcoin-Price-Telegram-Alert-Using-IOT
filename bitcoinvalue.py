import requests                 # for making HTTP requests
import json                     # library for handling JSON data
import time                     # module for sleep operation
import conf                     # config file




def get_bitcoin_price():
   URL = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD" # REPLACE WITH CORRECT URL
   response = requests.request("GET", URL)
   response = json.loads(response.text)
   current_price = response["USD"]
   return current_price


def send_telegram_message(message):
    """Sends message via Telegram"""
    url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": conf.telegram_chat_id,
        "text": message
    }
    try:
        response = requests.request(
            "GET",
            url,
            params=data
        )
        print("This is the Telegram response")
        print(response.text)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False

while True:
    # Step 1
    current_price = get_bitcoin_price()    
    print("The current value is:", current_price)
    
    if current_price >= conf.Max_bitcoin_val :
        print("Bitcoin Price Hike, Sell It!")
        message = "Alert! Bitcoin price has exceeded"+ str(conf.Max_bitcoin_val)  + \
                  ". The current price is " + str(current_price)
        telegram_status = send_telegram_message(message)
        print("This is the Telegram status:", telegram_status)
    elif current_price < conf.Min_bitcoin_val :
        print("Bitcoin Price Down, Invest!")
        message = "Alert! Bitcoin price has gone below "+ str(conf.Min_bitcoin_val) + \
                 ". The current price is " + str(current_price)
        telegram_status = send_telegram_message(message)
        print("This is Telegram Status:", telegram_status)

    time.sleep(30)
