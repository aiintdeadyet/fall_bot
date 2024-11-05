import requests
from tokens import PUSHOVER_API_TOKEN as API_TOKEN
from tokens import PUSHOVER_USER_KEY as USER_KEY


def send_pushover_notification(message):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": API_TOKEN,
        "user": USER_KEY,
        "message": message
    }
    response = requests.post(url, data=data)
    return response.status_code

# Fill in with your Pushover user key and API token
send_pushover_notification("Someone has fallen")

