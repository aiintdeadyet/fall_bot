# terminal app to get info to send a person notifications


def get_info():

    # name
    first_name = input("What is your first name: ")
    last_name  = input("What is your last name: ")
    name = first_name + " " + last_name

    # phone number
    phone_number = input("What is your phone number: ")

    # phone carryier
    phone_carryer = input("Who is your phone carryer: ")

    # email address
    email = input("What is your email address: ")

    # pushover
    print("If you don't have a pushover userkey you can create one at https://pushover.net/")
    pushoverID = input("What is your pushover userkey: ")



def main():
    print("hello world")
    # things we need
    # name
    # first_name = input("What is your first name: ")
    # last_name  = input("What is your last name: ")
    # name = first_name + " " + last_name

    # phone number
    # phone carryier
    # email address
    # pushover


if __name__ == "__main__":
    main()
