import telepot
import time
import RPi.GPIO as GPIO
import json


with open("botToken.json") as json_data:
	data =  json.load(json_data)

print(data)
bot_token=data['token_value']
bot = telepot.Bot(token= bot_token)
print(bot)

offset = 0
messages = bot.getUpdates(offset=offset, limit=100)

for message in messages:
    print(message)
    offset = message['update_id'] + 1

print(offset)

# Setting up Raspberry Port
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ledPin = 12
GPIO.setup(ledPin, GPIO.OUT)

print("ready to get commands")

while True:
    incoming_message = bot.getUpdates(offset=offset, limit=1, timeout=2)
    if len(incoming_message) != 0:
        message = bot.getUpdates(offset=offset, limit=1)[0]['message']
        cmd = message['text']
        chatId = message['chat']['id']
        offset += 1
        print(cmd)
        if cmd == "On":
            print("turning on light")
            GPIO.output(ledPin, GPIO.HIGH)
            bot.sendMessage(chat_id=chatId, text="turning light on.")
        elif cmd == "Off":
            print("turning off light")
            GPIO.output(ledPin, GPIO.LOW)
            bot.sendMessage(chat_id=chatId, text="turning light off.")
        elif cmd == "Shutdown":
            print("Shutting down bot program")
		#GPIO.output(ledPin, GPIO.LOW)
            GPIO.cleanup()
            bot.sendMessage(chat_id=chatId, text="Going for a nap.")
            exit()
        else:
            print("not valid command")
            bot.sendMessage(chat_id=chatId, text="you talkin to me?!")
    time.sleep(2)

