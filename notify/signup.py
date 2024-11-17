import json
import os


# Terminal app to get info to send a person notifications
class Person():
    def __init__(self) -> None:
        # Name
        first_name = input("What is your first name: ")
        last_name = input("What is your last name: ")
        self.name = first_name + " " + last_name

        # Phone number
        self.phone_number = input("What is your phone number: ")

        # Phone carrier
        print("Who is your phone carrier:")
        print("1: At&t")
        print("2: Verizon")
        print("3: Tmobile")
        print("4: Sprint")
        carrier_num = 0
        while True:
            try:
                self.phone_carrier = int(input("Please input the number next to your phone carryer: "))
            except ValueError:
                print("Invalid choice")
                continue
            if self.phone_carrier > 4 or self.phone_carrier < 0:
                print("Invalid choice")
                continue
            else:
                break
        carriers = ("At&t", "Verizon", "Tmobile", "Sprint")
        self.phone_carrier = carriers[carrier_num]

        # Email address
        self.email = input("What is your email address: ")

        # Pushover
        print("If you don't have a Pushover userkey, you can create one at https://pushover.net/")
        self.pushoverID = input("What is your Pushover userkey: ")

    def save_to_json(self, filename="people.json"):
        """Appends the person's data to a JSON file."""
        # Convert the person's attributes to a dictionary
        person_data = {
            "name": self.name,
            "phone_number": self.phone_number,
            "phone_carrier": self.phone_carrier,
            "email": self.email,
            "pushoverID": self.pushoverID
        }

        # Check if the file exists
        if os.path.exists(filename):
            # Read existing data and append new data
            with open(filename, "r") as json_file:
                try:
                    data = json.load(json_file)
                except json.JSONDecodeError:
                    data = []  # If file is empty, start with an empty list
        else:
            data = []

        # Append the new person's data
        data.append(person_data)

        # Write updated data back to the file
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"{self.name}'s information has been added to {filename}")


def main():
    # Create a person object
    new_person = Person()

    # Save the person's data to the JSON file
    new_person.save_to_json()


if __name__ == "__main__":
    main()
