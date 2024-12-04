import smtplib
from email.message import EmailMessage

from . import tokens
from .tokens import GMAIL_USERNAME as username
from .tokens import GMAIL_PASSWORD as password
from .tokens import PHONE_NUMBER  as number
from .tokens import GMAIL_APP_PASSWORD as app_password


def Email(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to
    msg["from"] = username

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(username, app_password)
    server.send_message(msg)

    server.quit()


def main():
    Email("Hello World", "Test message", "1234567890@tmomail.net")


if __name__ == "__main__":
    main()
