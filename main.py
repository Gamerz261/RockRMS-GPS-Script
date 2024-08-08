import requests
import csv

# Set up Rock RMS API details
api_base_url = "https://rock.gdlc.org/api"
login_url = f"{api_base_url}/auth/login"
username = "[REDACTED]"
password = "[REDACTED]"

# Function to authenticate and return a session
def authenticate():
    session = requests.Session()
    login_data = {
        "Username": username,
        "Password": password
    }
    login_response = session.post(login_url, json=login_data)
    
    # Check if login was successful
    if login_response.status_code != 200:
        raise Exception("Failed to log in, check your credentials or login endpoint.")
    
    return session

# Initialize session
session = authenticate()

# Function to search for person by first and last name
def search_person(first_name, last_name):
    global session  # Ensure the session is accessible
    
    url = f"{api_base_url}/People"
    params = {
        "FullName": first_name + " " + last_name
    }
    response = session.get(url, params=params)  # Use session to maintain the cookie
    
    # Check if session has expired
    if response.status_code == 401:
        print("Session expired, re-authenticating...")
        session = authenticate()  # Re-authenticate and get a new session
        response = session.get(url, params=params)  # Retry the request
    
    return response.json()

# Function to update person attributes
def update_person_attributes(person_id, attributes):
    global session  # Ensure the session is accessible
    
    url = f"{api_base_url}/AttributeValues"
    data = {
        "PersonId": person_id,
        "Attributes": attributes
    }
    response = session.post(url, json=data)  # Use session to maintain the cookie
    
    # Check if session has expired
    if response.status_code == 401:
        print("Session expired, re-authenticating...")
        session = authenticate()  # Re-authenticate and get a new session
        response = session.post(url, json=data)  # Retry the request
    
    return response.json()

# Read CSV file
csv_file_path = "./user_assessments.csv"

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    latest_records = {}

    # Iterate over rows in the CSV
    for row in csv_reader:
        first_name = row['first_name']
        last_name = row['last_name']
        key = (first_name, last_name)
        latest_records[key] = row  # Replace with the latest row for each name

# Process each unique name in the CSV
for (first_name, last_name), row in latest_records.items():
    matches = search_person(first_name, last_name)
    
    if len(matches) > 1:
        print(f"Multiple records found for {first_name} {last_name}")
    elif len(matches) == 0:
        print(f"No records found for {first_name} {last_name}")
    else:
        person_id = matches[0]['Id']
        
        # Extract attributes from CSV row
        attributes = {
            "GPSSpiritualGift1": row['spiritual_gift_1'],
            "GPSSpiritualGift2": row['spiritual_gift_2'],
            "GPSSpiritualGift3": row['spiritual_gift_3'],
            "GPSSpiritualGift4": row['spiritual_gift_4'],
            "GPSSpiritualGift1Score": row['spiritual_gift_1_score'],
            "GPSSpiritualGift2Score": row['spiritual_gift_2_score'],
            "GPSSpiritualGift3Score": row['spiritual_gift_3_score'],
            "GPSSpiritualGift4Score": row['spiritual_gift_4_score'],
            "GPSKeyAbilities1": row['key_abilities_1'],
            "GPSKeyAbilities2": row['key_abilities_2'],
            "GPSKeyAbilities3": row['key_abilities_3'],
            "GPSPassion1": row['passion_1'],
            "GPSPassion2": row['passion_2'],
            "GPSPassion3": row['passion_3'],
            "GPSPassion1Score": row['passion_1_score'],
            "GPSPassion2Score": row['passion_2_score'],
            "GPSPassion3Score": row['passion_3_score'],
            "GPSPeoplePassion1": row['people_passions_1'],
            "GPSPeoplePassion2": row['people_passions_2'],
            "GPSPeoplePassion3": row['people_passions_3'],
            "GPSCausePassion1": row['cause_passions_1'],
            "GPSCausePassion2": row['cause_passions_2'],
            "GPSCausePassion3": row['cause_passions_3']
        }

        # Update attributes for the matched person
        update_response = update_person_attributes(person_id, attributes)
        print(f"Updated attributes for {first_name} {last_name} (ID: {person_id})")
