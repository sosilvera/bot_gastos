import requests
import jmespath
import json
import env

def send_to_telegram(id, message):
    apiToken = env.TOKEN_GASTOS_BOT
    chatID = id
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        # print(response.text)
    except Exception as e:
        print(e)

def send_image(id, image_name):
    with open(image_name, 'rb') as image_file:
        files = {'photo': image_file.read()}
    
    apiToken = env.TOKEN_GASTOS_BOT
    chatID = id
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendPhoto?chat_id={chatID}'

    try:
        response = requests.post(apiURL, files=files)
        print(response.text)
    except Exception as e:
        print(e)



def get_messages():
    apiToken = env.TOKEN_GASTOS_BOT
    chatID = env.GASTOS_CHANNEL_ID
    apiURL = f'https://api.telegram.org/bot{apiToken}/getUpdates'

    try:
        response = requests.get(apiURL, json={'chat_id': chatID})
        # print(response.text)
        return response.text
    except Exception as e:
        print(e)

def get_last_message(body):
    data = json.loads(body)

    try:
        # Consulta JMESPath
        query = "result | sort_by(@, &message.date) | [-1].message"
        last_message = jmespath.search(query, data)

        formatted_message = {
            "name": last_message["from"]["first_name"],
            "lastName": last_message["from"]["last_name"],
            "userId": last_message["from"]["id"],
            "date": last_message["date"],
            "text": last_message["text"],
            "response": False
        }
    except Exception as e:
        formatted_message = {
            "name": None
        }
    return formatted_message