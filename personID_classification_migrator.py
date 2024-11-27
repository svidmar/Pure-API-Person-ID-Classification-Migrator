import requests
import pandas as pd
import logging
from datetime import datetime

# Configure logging
log_filename = f"api_update_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configuration
API_URL = "https://xyz.elsevierpure.com/ws/api/persons/"
API_KEY = "myapikey"

# Headers for GET and PUT requests
HEADERS = {
    "accept": "application/json",
    "api-key": API_KEY
}
PUT_HEADERS = {
    **HEADERS,
    "content-type": "application/json"
}

# Read Excel sheet
excel_file = "test.xlsx"  # Replace with your file path
data = pd.read_excel(excel_file)

# Iterate through each UUID
for _, row in data.iterrows():
    uuid = row['UUID']
    medarbejder_id = row['Medarbejder id']
    
    # Log the start of processing for this UUID
    logging.info(f"Processing UUID: {uuid} with Medarbejder ID: {medarbejder_id}")

    # GET request to fetch person data
    response = requests.get(f"{API_URL}{uuid}", headers=HEADERS)
    if response.status_code != 200:
        logging.error(f"Failed to fetch data for UUID: {uuid}. Status Code: {response.status_code}")
        continue

    person_data = response.json()
    identifiers = person_data.get("identifiers", [])
    logging.info(f"Original Identifiers for UUID {uuid}: {identifiers}")

    # Update identifiers where medarbejder ID matches
    updated_identifiers = []
    updated = False
    for identifier in identifiers:
        if identifier.get("id") == medarbejder_id and identifier.get("type", {}).get("uri") == "/dk/atira/pure/person/personsources/employee":
            # Log the change
            logging.info(
                f"Updating identifier for UUID: {uuid}, Original URI: {identifier['type']['uri']}, New URI: /dk/atira/pure/person/personsources/aauh_employee_id"
            )
            # Modify the URI for the matching identifier
            identifier["type"]["uri"] = "/dk/atira/pure/person/personsources/aauh_employee_id"
            updated = True
        updated_identifiers.append(identifier)

    if not updated:
        logging.warning(f"No matching Medarbejder ID found for UUID: {uuid}")
        continue

    # Prepare data for PUT request
    payload = {"identifiers": updated_identifiers}
    logging.info(f"PUT Payload for UUID {uuid}: {payload}")

    # PUT request to update person data
    put_response = requests.put(
        f"{API_URL}{uuid}",
        headers=PUT_HEADERS,
        json=payload
    )

    if put_response.status_code == 200:
        logging.info(f"Successfully updated UUID: {uuid}")
    else:
        logging.error(f"Failed to update UUID: {uuid}, Status Code: {put_response.status_code}, Response: {put_response.text}")
