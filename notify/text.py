from .send_email import Email


extentions = {
    "at&t": "@txt.att.net",
    "verizon": "@vtext.com",
    "tmobile": "@tmomail.net",
    "sprint": "@pm.sprint.com"
}


def text(number, carrier):
    extention = extentions[carrier.lower()]
    Email("From fall_bot", "Someone has fallen", str(number + extention))


def main():
    text("8013725518", "tmobile")


if __name__ == "__main__":
    main()
