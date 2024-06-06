# script Iterates over list of integration IDs - exports integrations to download dir
import os
import requests

# Replace these variables with your Oracle Integration Cloud details
OIC_INSTANCE = 'OIC INSTANCE'
OIC_USERNAME = 'USERNAME'
OIC_PASSWORD = 'PASSWORD'

# Set up session for persistent connection with authentication
session = requests.Session()
session.auth = (OIC_USERNAME, OIC_PASSWORD)

# API endpoint to retrieve integration IDs with a specific name pattern
integrations_url = f'https://{OIC_INSTANCE}/ic/api/integration/v1/integrations?q={{name:/INT_/,status:\'ACTIVATED\'}}'

# Local directory to save exported IAR files
export_directory = r'C:\Users\bryan\Downloads'

try:
    # Make the request to retrieve integration data
    response = session.get(integrations_url)
    response.raise_for_status()

    # Parse the response content as JSON
    integration_data = response.json()

    # Extract and export integrations with names starting with 'INT_'
    for integration in integration_data.get('items', []):
        if integration['code'].startswith('INT_'):
            # Extract integration code and version
            integration_code = integration['code']
            integration_version = integration['version']

            # Composite identifier {id} for export API
            integration_id = f"{integration_code}|{integration_version}"

            # API endpoint for exporting integration
            export_url = f'https://{OIC_INSTANCE}/ic/api/integration/v1/integrations/{integration_id}/archive'

            # Make the request to export the integration
            export_response = session.get(export_url)
            export_response.raise_for_status()

            # Save the exported IAR file to the local directory
            iar_filename = f"{integration_code}_{integration_version}.iar"
            iar_filepath = os.path.join(export_directory, iar_filename)

            with open(iar_filepath, 'wb') as iar_file:
                iar_file.write(export_response.content)

            print(f"Integration {integration_id} exported to {iar_filepath}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

finally:
    # Close the session
    session.close()
