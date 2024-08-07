import requests
import csv

# Set up Rock RMS API details
api_base_url = "https://your-rock-server/api"
api_key = "5vNqt7gnr8rOmCjeDHPONbzv"

# Function to search for person by first and last name
def search_person(first_name, last_name):
    url = f"{api_base_url}/People"
    params = {
        "FirstName": first_name,
        "LastName": last_name
    }
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

# Function to update person attributes
def update_person_attributes(person_id, attributes):
    url = f"{api_base_url}/AttributeValues"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "PersonId": person_id,
        "Attributes": attributes
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Read CSV file
csv_file_path = "./user_assesments.csv"

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    latest_records = {}

    # Iterate over rows in the CSV
    for row in csv_reader:
        first_name = row['first_name']
        last_name = row['last_name']
        key = (first_name, last_name)
        latest_records[key] = row  # Replace with latest row for each name

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
            "GPSSpiritualGift1": row['GPSSpiritualGift1'],
            "GPSSpiritualGift2": row['GPSSpiritualGift2'],
            "GPSSpiritualGift3": row['GPSSpiritualGift3'],
            "GPSSpiritualGift1Score": row['GPSSpiritualGift1Score'],
            "GPSSpiritualGift2Score": row['GPSSpiritualGift2Score'],
            "GPSSpiritualGift3Score": row['GPSSpiritualGift3Score'],
            "GPSSpiritualGift4Score": row['GPSSpiritualGift4Score'],
            "GPSKeyAbilities1": row['GPSKeyAbilities1'],
            "GPSKeyAbilities2": row['GPSKeyAbilities2'],
            "GPSKeyAbilities3": row['GPSKeyAbilities3'],
            "GPSPassion1": row['GPSPassion1'],
            "GPSPassion2": row['GPSPassion2'],
            "GPSPassion3": row['GPSPassion3'],
            "GPSPeoplePassion1": row['GPSPeoplePassion1'],
            "GPSPeoplePassion2": row['GPSPeoplePassion2'],
            "GPSPeoplePassion3": row['GPSPeoplePassion3'],
            "GPSCausePassion1": row['GPSCausePassion1'],
            "GPSCausePassion2": row['GPSCausePassion2'],
            "GPSCausePassion3": row['GPSCausePassion3']
        }

        # Update attributes for the matched person
        update_response = update_person_attributes(person_id, attributes)
        print(f"Updated attributes for {first_name} {last_name} (ID: {person_id})")
