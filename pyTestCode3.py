# script Iterates over list of integration IDs - returns integration name and integration version
import requests

# Replace these variables with your Oracle Integration Cloud details
OIC_INSTANCE = 'OIC INSTANCE'
OIC_USERNAME = 'USERNAME'
OIC_PASSWORD = 'PASSWORD'

# Set up session for persistent connection with authentication
session = requests.Session()
session.auth = (OIC_USERNAME, OIC_PASSWORD)
# parameters = '{name: /INT_/, status: "ACTIVATED"}'

# API endpoint to retrieve integration IDs with a specific name pattern
integrations_url = f'https://{OIC_INSTANCE}/ic/api/integration/v1/integrations?q={{name:/INT_/,status:\'ACTIVATED\'}}'

try:

    # Make the request to retrieve integration data
    response = session.get(integrations_url)
    response.raise_for_status()

    # Parse the response content as JSON
    integration_data = response.json()

    # Extract integration names and versions starting with 'INT_'
    integrations_info = [
        f"{integration['name']}|{integration['version']}"
        for integration in integration_data.get('items', [])
        if integration['name'].startswith('INT_')
    ]

    # Print or use the filtered integration info as needed
    for integration_info in integrations_info:
        print("Integration Info:", integration_info)

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

finally:
    # Close the session
    session.close()