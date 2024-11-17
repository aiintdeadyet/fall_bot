import json
import send_email
import text
import pushover


def load_people(filename="people.json"):
    """Loads the people information from a JSON file."""
    try:
        with open(filename, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please ensure the file exists.")
        return []
    except json.JSONDecodeError:
        print(f"Error: {filename} is not a valid JSON file.")
        return []


def notify(person_name, people_data):
    """Notify the passed-in person with the method they want to be notified."""
    # Find the person's information
    person_info = next((p for p in people_data if p["name"] == person_name), None)
    if not person_info:
        print(f"Error: No information found for {person_name}.")
        return

    # Notify via pushover
    if person_info["pushoverID"]:
        pushover.pushover(person_info["pushoverID"])

    # Notify via email
    if person_info["email"]:
        send_email.Email("Fall bot", "Someone has fallen", person_info["email"])

    # Notify via text
    if person_info["phone_number"] and person_info["phone_carrier"]:
        text.text(person_info["phone_number"], person_info["phone_carrier"])


def main():
    # Load people data from the JSON file
    people_data = load_people()

    # Notify individuals
    notify("James", people_data)
    # Uncomment to notify others:
    # notify("Bailey", people_data)
    # notify("Zach", people_data)


if __name__ == "__main__":
    main()
