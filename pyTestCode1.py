# script Iterates over list of integration IDs - returns all data about each integration that has 'INT_'
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

    """""
    # Make the request to retrieve integration IDs
    response = session.get(integrations_url)
    response.raise_for_status()


    # Print the response content to examine its structure
    print("API Response Content:")
    print(response.text)

    # Extract integration IDs from the response
    #integration_data = response.json()
    #integration_ids = [integration['id'] for integration in integration_data]

    # Print or use the integration IDs as needed
    #print("Integration IDs:", integration_ids)
    """""

    # Make the request to retrieve integration data
    response = session.get(integrations_url)
    response.raise_for_status()

    # Print the response content to examine its structure
    print("API Response Content:")
    print(response.text)

    # Parse the response content as JSON
    integration_data = response.json()

    # Extract integration names starting with 'INT_'
    integration_names = [integration['name'] for integration in integration_data.get('items', []) if
                         integration['name'].startswith('INT_')]

    # Print or use the filtered integration names as needed
    print("Integration Names starting with 'INT_':", integration_names)

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

finally:
    # Close the session
    session.close()
