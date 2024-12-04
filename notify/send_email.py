import smtplib
from email.message import EmailMessage

from . import tokens
from .tokens import GMAIL_USERNAME as username
from .tokens import GMAIL_PASSWORD as password
from .tokens import PHONE_NUMBER  as number
from .tokens import GMAIL_APP_PASSWORD as app_password


# def Email(subject, body, to):
#     msg = EmailMessage()
#     msg.set_content(body)
#     msg["subject"] = subject
#     msg["to"] = to
#     msg["from"] = username

#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(username, app_password)
#     server.send_message(msg)

#     server.quit()

def Email(subject, body, to, attachment_path=None):
    """
    Sends an email with an optional attachment.
    
    Args:
        subject (str): Email subject.
        body (str): Email body.
        to (str): Recipient's email address.
        attachment_path (str): Path to the attachment file (optional).
    """
    # Create the email
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to
    msg["from"] = username

    # Add an attachment if specified
    if attachment_path:
        try:
            with open(attachment_path, "rb") as attachment:
                file_data = attachment.read()
                file_name = attachment_path.split("/")[-1]  # Extract the file name
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
        except FileNotFoundError:
            print(f"Error: The file '{attachment_path}' was not found.")
            return

    # Connect to Gmail's SMTP server and send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(username, app_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {to} with attachment: {attachment_path}")
    except Exception as e:
        print(f"Error: Unable to send email. {e}")


def main():
    Email("Hello World", "Test message", "1234567890@tmomail.net")


if __name__ == "__main__":
    main()
