from people_info import contact_info
import send_email
import text
import pushover


def notify(person):
    """notify the passed in person with the method they want to be notifyed"""
    person_info = contact_info[person]
    if person_info["pushover"][0] and person_info["pushover"][1]:
        pushover.pushover(person_info["pushover"])
    if person_info["email"][0] and person_info["email"][1]:
        print(person_info["email"][0])
    if person_info["phone"][0] and person_info["phone"][1]:
        text.text(person_info["phone"][0], person_info["phone"][2])


def main():
    notify("James")


if __name__ == "__main__":
    main()
