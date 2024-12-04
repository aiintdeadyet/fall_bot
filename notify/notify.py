import json
import os
from . import send_email
from . import text
from . import pushover


def load_people(filename="people.json"):
    """Loads the people information from a JSON file."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Get directory of the script
        file_path = os.path.join(current_dir, filename)  # Construct absolute path
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please ensure the file exists.")
        return []
    except json.JSONDecodeError:
        print(f"Error: {filename} is not a valid JSON file.")
        return []


def notify(person_name, fall_video=None):
    """Notify the passed-in person with the method they want to be notified."""
    people_data = load_people()

    # Find the person's information
    person_info = next((p for p in people_data if p["name"] == person_name), None)
    if not person_info:
        print(f"Error: No information found for {person_name}.")
        return

    # Notify via pushover if opted in
    if person_info.get("pushover_opt_in") and person_info["pushoverID"]:
        pushover.pushover(person_info["pushoverID"])
        print(f"Pushover notification sent to {person_name}.")

    # Notify via email if opted in
    if person_info.get("email_opt_in") and person_info["email"]:
        send_email.Email("Fall bot", "Someone has fallen", person_info["email"], fall_video)
        print(f"Email notification sent to {person_name}.")

    # Notify via text if opted in
    if person_info.get("sms_opt_in") and person_info["phone_number"] and person_info["phone_carrier"]:
        text.text(person_info["phone_number"], person_info["phone_carrier"])
        print(f"SMS notification sent to {person_name}.")


def main():
    # Notify individuals
    notify("James Critchlow")
    # notify("Bailey Haskell")
    # Uncomment to notify others:
    # notify("Bailey")
    # notify("Zach")


if __name__ == "__main__":
    main()
