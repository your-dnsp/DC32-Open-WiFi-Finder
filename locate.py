import requests
import base64

# Coordinates of key locations for DEF CON 32
locations = {
    1: {"name": "Las Vegas Convention Center", "lat": 36.1290, "lon": -115.1537},
    2: {"name": "Resort World", "lat": 36.1350, "lon": -115.1600},
    3: {"name": "Rio Hotel and Casino", "lat": 36.1164, "lon": -115.1881},
    4: {"name": "Sahara", "lat": 36.1422, "lon": -115.1544},
    5: {"name": "Fontainebleau", "lat": 36.1363, "lon": -115.1634},
    6: {"name": "Tuscany Hotel", "lat": 36.1118, "lon": -115.1569},
    7: {"name": "Las Vegas Airport", "lat": 36.0840, "lon": -115.1537},
    8: {"name": "The Westin", "lat": 36.1195, "lon": -115.1672},
    9: {"name": "Taco Bell Cantina", "lat": 36.1171, "lon": -115.1722},
    10: {"name": "Westgate Las Vegas", "lat": 36.1360, "lon": -115.1518},
    11: {"name": "MGM Grand", "lat": 36.1026, "lon": -115.1703},
    12: {"name": "The Mirage", "lat": 36.1216, "lon": -115.1745},
    13: {"name": "Caesars Palace", "lat": 36.1178, "lon": -115.1745},
    14: {"name": "Bellagio Hotel", "lat": 36.1126, "lon": -115.1763},
    15: {"name": "Mandalay Bay", "lat": 36.0909, "lon": -115.1761},
    16: {"name": "Luxor Hotel", "lat": 36.0958, "lon": -115.1761},
    17: {"name": "New York-New York Hotel", "lat": 36.1024, "lon": -115.1748},
    18: {"name": "The Venetian", "lat": 36.1216, "lon": -115.1694},
    19: {"name": "Wynn Las Vegas", "lat": 36.1273, "lon": -115.1655},
    20: {"name": "Treasure Island", "lat": 36.1245, "lon": -115.1703}
}

def get_wifi_networks(lat, lon, radius, api_name, api_token):
    """
    Fetch Wi-Fi networks in a given radius from the specified latitude and longitude using the Wigle.net API.
    
    Args:
    lat (float): Latitude of the center point.
    lon (float): Longitude of the center point.
    radius (int): Radius in meters to search for networks.
    api_name (str): API name (username) for Wigle.net.
    api_token (str): API token for Wigle.net.
    
    Returns:
    dict: Parsed JSON response from the Wigle.net API.
    
    Raises:
    ValueError: If the data cannot be fetched.
    """
    url = "https://api.wigle.net/api/v2/network/search"
    params = {
        "latrange1": lat - (radius / 111320),  # Convert radius to lat/lon degrees
        "latrange2": lat + (radius / 111320),
        "longrange1": lon - (radius / 111320),
        "longrange2": lon + (radius / 111320),
        "freenet": "true",
        "resultsPerPage": 100
    }
    auth = base64.b64encode(f"{api_name}:{api_token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Failed to fetch data: {response.status_code}, {response.text}")

# Function to display open networks and count the number of unique SSIDs
def display_open_networks(networks):
    """
    Display unique open Wi-Fi networks and their SSIDs.
    
    Args:
    networks (list): List of networks from Wigle.net API.
    """
    if not networks:
        print("No open networks found.")
        return

    print("Open Wi-Fi networks:")
    unique_ssids = set()
    for network in networks:
        ssid = network.get("ssid", "N/A")
        if ssid not in unique_ssids:
            unique_ssids.add(ssid)
            print(f"SSID: {ssid}")

    ssid_count = len(unique_ssids)
    print(f"\nTotal unique SSIDs found: {ssid_count}")

    # Report the number of networks found
    if ssid_count == 0:
        print("No networks found near you.")
    elif 1 <= ssid_count <= 3:
        print("A few networks found near you.")
    elif 4 <= ssid_count <= 7:
        print("Some networks found near you.")
    elif 8 <= ssid_count <= 10:
        print("Lots of networks found near you.")
    else:
        print("Stumbler's paradise! Lots of networks found near you.")

# Main function to get user input and provide open networks
def main():
    """
    Main function to interact with the user, get the API credentials, and display open networks around selected locations.
    """
    print("Select a location:")
    for key, location in locations.items():
        print(f"{key} - {location['name']}")
    
    try:
        choice = int(input("Enter the number corresponding to your location: "))
        if choice not in locations:
            raise ValueError("Invalid choice. Please select a valid location number.")
        
        api_name = input("Enter your Wigle.net API name: ")
        api_token = input("Enter your Wigle.net API token: ")

        selected_location = locations[choice]
        lat = selected_location["lat"]
        lon = selected_location["lon"]
        radius = 500  # Search within 0.5 km radius

        networks_data = get_wifi_networks(lat, lon, radius, api_name, api_token)
        networks = networks_data.get('results', [])
        display_open_networks(networks)
    
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
