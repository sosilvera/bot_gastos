import commons.telegramLib as t
import time
from commons.bot import Bot
from transformers import pipeline

lastMsgHour = 0
needResponse = False

model = "facebook/bart-large-mnli"
classifier = pipeline("zero-shot-classification", model=model)

while True:
    lastMsg = t.get_last_message(t.get_messages())
    
    if lastMsg["name"] != None and lastMsgHour != lastMsg["date"]:
        if needResponse:
            lastMsg["response"] = True

        print("Entro a responder")
        lastMsgHour = lastMsg["date"]
        responseMsg = Bot(lastMsg, classifier).getResponse()

        if responseMsg["image"]:
            t.send_image(lastMsg["userId"], responseMsg["msg"])
        else:
            t.send_to_telegram(lastMsg["userId"], responseMsg["msg"])
        
        needResponse = responseMsg["need_response"]
    print("Vuelvo a consultar")
    time.sleep(1)