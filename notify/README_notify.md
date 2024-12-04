# Documentation: Notification Signup and Triggering System

This documentation explains how to use the notification system, which consists of two scripts:

1. **`notify/signup.py`** : Used to sign up individuals for notifications.
2. **`notify/notify.py`** : Used to send notifications to signed-up individuals based on their preferences.

### Project Structure

fallbot/
└── notify/
    ├── signup.py          # Script for signing up individuals
    ├── notify.py          # Script for sending notifications
    ├── send_email.py      # Handles email notifications
    ├── text.py            # Handles SMS notifications
    ├── pushover.py        # Handles Pushover notifications
    └── people.json        # Stores signed-up individuals and their preferences

### How It Works

#### 1. **Signing Up Individuals**

Run the `signup.py` script to collect information from individuals who want to receive notifications.

* The script will ask for:
  * **Name** (first and last)
  * **Phone number** and **carrier**
  * **Email address**
  * **Pushover user key**
* The script will also ask if the individual wants to receive notifications via:
  * **SMS**
  * **Email**
  * **Pushover**

The collected data is stored in the `people.json` file, along with the individual's notification preferences.

##### Example:

``python signup.py``

Follow the prompts to input the user's information.


#### 2. **Sending Notifications**

To send a notification, use the `notify()` function from the `notify/notify.py` file. You can call this function from another Python script in the project. 

***NOTE: If using email you need to add a tokens.py file in the notify directory. You can follow this link to setup email. The file structure for tokens.py will be like the following. https://www.youtube.com/watch?v=hXiPshHn9Pw&t=5s***


## Example Code

```python
# tokens.py

# Pushover Example Code
PUSHOVER_API_TOKEN = "YOUR API TOKEN"
PUSHOVER_USER_KEY = "YOUR USER KEY"

# Gmail Info Example Code
GMAIL_USERNAME = "YOUR GMAIL USERNAME"
GMAIL_PASSWORD = "YOUR GMAIL PASSWORD"
PHONE_NUMBER = "YOUR PHONE NUMBER"
GMAIL_APP_PASSWORD = "YOUR GMAIL APP PASSWORD"
```
##### Importing the `notify` Function

In your script, import the `notify` function like this:

``from notify.notify import notify``

##### Using the `notify` Function

Call the `notify` function with the name of the person you want to notify. The function will:

1. Look up the individual's information in `people.json`.
2. Send notifications via the methods they opted into (SMS, Email, Pushover).

##### Example:

```
from notify.notify import notify

# Notify James
notify("James")
```


### File Descriptions

#### `notify/signup.py`

* **Purpose** : Collects information about individuals who want to sign up for notifications.
* **Output** : Appends data to `people.json`.

#### `notify/notify.py`

* **Purpose** : Sends notifications to individuals based on their preferences.
* **Functions** :
* `load_people(filename="people.json")`: Loads the `people.json` file.
* `notify(person_name)`: Sends notifications to the specified individual.

#### `notify/send_email.py`

* Handles sending email notifications. Called by `notify.py`.

#### `notify/text.py`

* Handles sending SMS notifications. Called by `notify.py`.

#### `notify/pushover.py`

* Handles sending Pushover notifications. Called by `notify.py`.

#### `notify/people.json`

* A JSON file that stores user data and notification preferences.


### Notes

* Make sure `people.json` is present in the notify directory before calling the `notify` function.
* Ensure that all notification modules (`send_email.py`, `text.py`, `pushover.py`) are properly configured and have all their dependencies installed through pip.
* Make sure you have a pushover user account and you have the pushover app downloaded if you want to recive notifications through pushover.
