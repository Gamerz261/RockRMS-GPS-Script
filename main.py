import requests
import csv

# Set up Rock RMS API details
api_base_url = "https://rock.gdlc.org/api"
login_url = f"{api_base_url}/Auth/Login"
username = "/*REDACTED*/"
password = "/*REDACTED*/"


# Function to authenticate and return a session
def authenticate():
    session = requests.Session()
    login_data = {
        "Username": username,
        "Password": password,
        "Persisted": True
    }
    login_response = session.post(login_url, json=login_data)
    
    # Check if login was successful
    if login_response.status_code != 204:
        raise Exception("Failed to log in, check your credentials or login endpoint.")
    
    return session

# Initialize session
session = authenticate()

# Function to search for person by first and last name
def get_people():
    global session  # Ensure the session is accessible
    
    url = f"{api_base_url}/People?$select=FirstName,LastName,Id"
    params = {}
    response = session.get(url, params=params)  # Use session to maintain the cookie
    
    # Check if session has expired
    if response.status_code == 401:
        print("Session expired, re-authenticating...")
        session = authenticate()  # Re-authenticate and get a new session
        response = session.get(url, params=params)  # Retry the request
    
    return response.json()

def get_matches(personList, firstName, lastName):
    count = 0
    Id = None
    
    for record in personList:
        if firstName == record['FirstName'] and lastName == record['LastName']:
            Id = record['Id']
            count += 1

    return Id, count

def post_api_vals(url, person_id, attributeKey, attributeValue):
    global session  # Ensure the session is accessible
    #data = {
    #    "Id": person_id,
    #    "AttributeKey": f"{attributeKey}",
    #    "AttributeValue": f"{attributeValue}"
    #}
    #print(data)
    #print(f"{api_base_url}/People/AttributeValue/{person_id}?attributeKey={attributeKey}&attributeValue={attributeValue}")

    # Determine if there is a value to put in
    if attributeValue != '':
        response = session.post(f"{api_base_url}/People/AttributeValue/{person_id}?attributeKey={attributeKey}&attributeValue={attributeValue}")  # Use session to maintain the cookie
    else:
        print(f"Skipping {attributeKey} because AttributeValue = \'{attributeValue}\' (null)!")
        return


    # Check if session has expired
    if response.status_code == 401:
        print("Session expired, re-authenticating...")
        session = authenticate()  # Re-authenticate and get a new session
        response = session.post(f"{api_base_url}/People/AttributeValue/{person_id}?attributeKey={attributeKey}&attributeValue={attributeValue}")  # Retry the request

    # Check if the response has a JSON body
    if (response.status_code == 200) or (response.status_code == 202):
        if response.headers.get('Content-Type') == 'application/json' and response.content:
            return response.json()
        else:
            return response.text  # or handle non-JSON response
    elif response.status_code == 204:
        print("Update successful, but no content returned.")
        return None
    else:
        raise Exception("Push failed with status code: " + str(response.status_code))

# Function to update person attributes
def update_person_attributes(person_id, attributes):
    global session  # Ensure the session is accessible
    
    #This literally won't be used at all but it's a pain in the ass to delete so I'm gonna leave it here
    url = f"{api_base_url}/AttributeValues/AttributeValue/11841/POSTapi_AttributeValues_AttributeValue_idattributeKeyattributeKeyattributeValueattributeValue"

    post_api_vals(url, person_id, "GPSSpiritualGift1", attributes['GPSSpiritualGift1'])
    post_api_vals(url, person_id, "GPSSpiritualGift1Score", attributes['GPSSpiritualGift1Score'])
    post_api_vals(url, person_id, "GPSSpiritualGift2", attributes['GPSSpiritualGift2'])
    post_api_vals(url, person_id, "GPSSpiritualGift2Score", attributes['GPSSpiritualGift2Score'])
    post_api_vals(url, person_id, "GPSSpiritualGift3", attributes['GPSSpiritualGift3'])
    post_api_vals(url, person_id, "GPSSpiritualGift3Score", attributes['GPSSpiritualGift3Score'])
    post_api_vals(url, person_id, "GPSSpiritualGift4", attributes['GPSSpiritualGift4'])
    post_api_vals(url, person_id, "GPSSpiritualGift4Score", attributes['GPSSpiritualGift4Score'])
    post_api_vals(url, person_id, "GPSKeyAbilities1", attributes['GPSKeyAbilities1'])
    post_api_vals(url, person_id, "GPSKeyAbilities2", attributes['GPSKeyAbilities2'])
    post_api_vals(url, person_id, "GPSKeyAbilities3", attributes['GPSKeyAbilities3'])
    post_api_vals(url, person_id, "GPSPassion1", attributes['GPSPassion1'])
    post_api_vals(url, person_id, "GPSPassion2", attributes['GPSPassion2'])
    post_api_vals(url, person_id, "GPSPassion3", attributes['GPSPassion3'])
    post_api_vals(url, person_id, "GPSPassion1Score", attributes['GPSPassion1Score'])
    post_api_vals(url, person_id, "GPSPassion2Score", attributes['GPSPassion2Score'])
    post_api_vals(url, person_id, "GPSPassion3Score", attributes['GPSPassion3Score'])
    post_api_vals(url, person_id, "GPSPeoplePassion1", attributes['GPSPeoplePassion1'])
    post_api_vals(url, person_id, "GPSPeoplePassion2", attributes['GPSPeoplePassion2'])
    post_api_vals(url, person_id, "GPSPeoplePassion3", attributes['GPSPeoplePassion3'])
    post_api_vals(url, person_id, "GPSCausePassion1", attributes['GPSCausePassion1'])
    post_api_vals(url, person_id, "GPSCausePassion2", attributes['GPSCausePassion2'])
    post_api_vals(url, person_id, "GPSCausePassion3", attributes['GPSCausePassion3'])

# Read CSV file
csv_file_path = "user_assesments_new.csv"

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
people = get_people()
for (first_name, last_name), row in latest_records.items():
    person_id, count = get_matches(people, first_name, last_name)
    
    if count > 1:
        print(f"Multiple records found for {first_name} {last_name}\n")
    elif count == 0:
        print(f"No records found for {first_name} {last_name}\n")
    else:
        print(f"Match found for {first_name} {last_name} at ID={person_id}! Pushing attributes...")
        
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
        print(f"Updated attributes for {first_name} {last_name} (ID: {person_id})\n")
