#imports all integrations starting in INT_ and of lockedFlag false. Still having some issues getting all integrations exported
#seems there is a pagination limit. Oracle Integration Cloud API is limiting the number of items we can download at each request
#This limit prevents an API from returning an excessive amount of data in one response.

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

# API endpoint to retrieve integration IDs with a specific name pattern and lockedFlag is false
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

try:
    # Make sure the backup folder exists, create it if not
    os.makedirs(backup_folder_path, exist_ok=True)

    # Make the request to retrieve integration data
    response = session.get(integrations_url)
    response.raise_for_status()

    # Parse the response content as JSON
    integration_data = response.json()

    # Open the text file for writing
    with open(exported_info_filepath, 'w') as exported_info_file:
        # Write header to the text file
        exported_info_file.write("Code Name | Integration Version | Status | Last Updated Date\n")

        # Extract and export integrations with names starting with 'INT_' and lockedFlag is false
        for integration in integration_data.get('items', []):
            # Add a condition to check if lockedFlag is false
            if integration['name'].startswith('INT_') and not integration['lockedFlag']:
                # Extract integration code, version, and status
                integration_code = integration['code']
                integration_version = integration['version']
                integration_status = integration['status']

                # Write information to the text file
                exported_info_file.write(
                    f"{integration_code} | {integration_version} | {integration_status} | {integration['lastUpdated']}\n")

                # Composite identifier {id} for export API
                integration_id = f"{integration_code}|{integration_version}"

                # API endpoint for exporting integration
                export_url = f'https://{OIC_INSTANCE}/ic/api/integration/v1/integrations/{integration_id}/archive'

                # Make the request to export the integration
                export_response = session.get(export_url)
                export_response.raise_for_status()

                # Save the exported IAR file to the backup folder
                iar_filename = f"{integration_code}_{integration_version}.iar"
                iar_filepath = os.path.join(backup_folder_path, iar_filename)

                with open(iar_filepath, 'wb') as iar_file:
                    iar_file.write(export_response.content)

                print(f"Integration {integration_id} exported to {iar_filepath}")

    print(f"Exported integrations info saved to {exported_info_filepath}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

finally:
    # Close the session
    session.close()
