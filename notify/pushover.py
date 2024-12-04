import requests
from .tokens import PUSHOVER_API_TOKEN as API_TOKEN
from .tokens import PUSHOVER_USER_KEY as USER_KEY


def pushover(userkey):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": API_TOKEN,
        "user": USER_KEY,
        "message": "Someone has fallen"
    }
    response = requests.post(url, data=data)
    return response.status_code

def main():
    # Fill in with your Pushover user key and API token
    pushover(USER_KEY)


if __name__ == "__main__":
    main()
