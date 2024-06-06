#To retrieve more items, I implemented pagination in my script.
#The Oracle Integration Cloud API supports pagination through the use of the limit and offset parameters.
#NOTE: this version only paginates up to 100 integrations

import os
import requests
from datetime import datetime

# Replace these variables with your Oracle Integration Cloud details
OIC_INSTANCE = 'OIC INSTANCE'
OIC_USERNAME = 'USERNAME'
OIC_PASSWORD = 'PASSWORD'

# Set up session for persistent connection with authentication
session = requests.Session()
session.auth = (OIC_USERNAME, OIC_PASSWORD)

# API endpoint to retrieve integration IDs with a specific name pattern
integrations_url = f'https://{OIC_INSTANCE}/ic/api/integration/v1/integrations?q={{name:/INT_/}}'

# Local directory to save exported IAR files
export_directory = os.path.expanduser('~/Downloads')

# Generate current date for use in file names
current_date = datetime.now().strftime('%Y%m%d%H%M')

# Create a folder with the current date and time
backup_folder_name = f'OICBACKUP_{current_date}'
backup_folder_path = os.path.join(export_directory, backup_folder_name)

# File path for the exported integrations info text file
exported_info_filename = f'exported_integrations_info_{current_date}.txt'
exported_info_filepath = os.path.join(backup_folder_path, exported_info_filename)

# Define pagination parameters
limit = 100  # Adjust this based on your needs
offset = 0

try:
    # Make sure the backup folder exists, create it if not
    os.makedirs(backup_folder_path, exist_ok=True)

    while True:
        # Make the request to retrieve integration data with pagination
        response = session.get(f'{integrations_url}&limit={limit}&offset={offset}')
        response.raise_for_status()

        # Parse the response content as JSON
        integration_data = response.json()

        # Exit the loop if there are no more items
        if not integration_data.get('items'):
            break

        # Open the text file for writing (append mode to avoid overwriting in each iteration)
        with open(exported_info_filepath, 'a') as exported_info_file:
            for integration in integration_data['items']:
                if integration['name'].startswith('INT_') and not integration['lockedFlag']:
                    integration_code = integration['code']
                    integration_version = integration['version']
                    integration_status = integration['status']
                    exported_info_file.write(
                        f"{integration_code} | {integration_version} | {integration_status} | {integration['lastUpdated']}\n")

                    integration_id = f"{integration_code}|{integration_version}"
                    export_url = f'https://{OIC_INSTANCE}/ic/api/integration/v1/integrations/{integration_id}/archive'

                    export_response = session.get(export_url)
                    export_response.raise_for_status()

                    iar_filename = f"{integration_code}_{integration_version}.iar"
                    iar_filepath = os.path.join(backup_folder_path, iar_filename)

                    with open(iar_filepath, 'wb') as iar_file:
                        iar_file.write(export_response.content)

                    print(f"Integration {integration_id} exported to {iar_filepath}")

        # Increment the offset for the next request
        offset += limit

    print(f"Exported integrations info saved to {exported_info_filepath}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

finally:
    # Close the session
    session.close()
