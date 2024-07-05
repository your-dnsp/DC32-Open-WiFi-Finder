import requests
import base64

# Coordinates of key locations for DEF CON 32 sorted by proximity to Las Vegas Convention Center
locations = {
    1: {"name": "Las Vegas Convention Center", "lat": 36.1290, "lon": -115.1537},
    2: {"name": "Westgate Las Vegas", "lat": 36.1360, "lon": -115.1518},
    3: {"name": "Resort World", "lat": 36.1350, "lon": -115.1600},
    4: {"name": "Tuscany Hotel", "lat": 36.1118, "lon": -115.1569},
    5: {"name": "The Mirage", "lat": 36.1216, "lon": -115.1745},
    6: {"name": "Wynn Las Vegas", "lat": 36.1273, "lon": -115.1655},
    7: {"name": "The Venetian", "lat": 36.1216, "lon": -115.1694},
    8: {"name": "The Palazzo", "lat": 36.1243, "lon": -115.1695},
    9: {"name": "Treasure Island", "lat": 36.1245, "lon": -115.1703},
    10: {"name": "High Roller", "lat": 36.1208, "lon": -115.1686},
    11: {"name": "The LINQ Hotel + Experience", "lat": 36.1189, "lon": -115.1681},
    12: {"name": "The Westin", "lat": 36.1195, "lon": -115.1672},
    13: {"name": "Fashion Show Mall", "lat": 36.1273, "lon": -115.1702},
    14: {"name": "Caesars Palace", "lat": 36.1178, "lon": -115.1745},
    15: {"name": "Planet Hollywood", "lat": 36.1095, "lon": -115.1703},
    16: {"name": "Bellagio Hotel", "lat": 36.1126, "lon": -115.1763},
    17: {"name": "Paris Las Vegas", "lat": 36.1126, "lon": -115.1701},
    18: {"name": "Aria Resort & Casino", "lat": 36.1070, "lon": -115.1763},
    19: {"name": "The Cosmopolitan", "lat": 36.1097, "lon": -115.1741},
    20: {"name": "Miracle Mile Shops", "lat": 36.1091, "lon": -115.1711},
    21: {"name": "The Park", "lat": 36.1037, "lon": -115.1740},
    22: {"name": "New York-New York Hotel", "lat": 36.1024, "lon": -115.1748},
    23: {"name": "MGM Grand", "lat": 36.1026, "lon": -115.1703},
    24: {"name": "Eataly Las Vegas", "lat": 36.1062, "lon": -115.1704},
    25: {"name": "Mandalay Bay", "lat": 36.0909, "lon": -115.1761},
    26: {"name": "Luxor Hotel", "lat": 36.0958, "lon": -115.1761},
    27: {"name": "Rio Hotel and Casino", "lat": 36.1164, "lon": -115.1881},
    28: {"name": "Sahara", "lat": 36.1422, "lon": -115.1544},
    29: {"name": "Fontainebleau", "lat": 36.1363, "lon": -115.1634},
    30: {"name": "Taco Bell Cantina", "lat": 36.1171, "lon": -115.1722},
    31: {"name": "Encore at Wynn Las Vegas", "lat": 36.1289, "lon": -115.1627},
    32: {"name": "Las Vegas Airport", "lat": 36.0840, "lon": -115.1537}
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
        "latrange2": lat + (radius / 111320),  # on the average distance covered by one degree of latitude
        "longrange1": lon - (radius / 111320), # which is approximately 111.32 kilometers (or 111,320 meters)
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

# Function to display the sassy reply
def display_sassy_reply():
    """
    Display a sassy reply with ASCII art for invalid inputs.
    """
    sassy_reply = [
        "----",
        ">(')____,  >(')____,  >(')____,  >(')____,  >(') ___,",
        " (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/",
        "~~~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~dnsp",
        "Don't try to hack me! That's rude!",
        "I can't blame you for your curiosity, that's what hackers do.",
        "----"
    ]
    for line in sassy_reply:
        print(line)

# Function to display location options in two columns
def display_location_options():
    """
    Display the location options in two columns.
    """
    keys = list(locations.keys())
    half = len(keys) // 2
    for i in range(half):
        left = f"{keys[i]} - {locations[keys[i]]['name']}"
        right = f"{keys[half + i]} - {locations[keys[half + i]]['name']}" if half + i < len(keys) else ""
        print(f"{left:<35} {right}")

# Main function to get user input and provide open networks
def main():
    """
    Main function to interact with the user, get the API credentials, and display open networks around selected locations.
    """
    while True:
        print("\nSelect a location:")
        display_location_options()
        print("0 - Quit")
        
        try:
            choice = input("Enter the number corresponding to your location: ")
            if choice == "0":
                print("Exiting...")
                break
            if not choice.isdigit() and choice not in ["yes", "no", "y", "n"]:
                display_sassy_reply()
                continue
            if choice.isdigit():
                choice = int(choice)
                if choice not in locations:
                    print("Invalid choice. Please select a valid location number.")
                    continue

                api_name = input("Enter your Wigle.net API name: ")
                api_token = input("Enter your Wigle.net API token: ")

                selected_location = locations[choice]
                lat = selected_location["lat"]
                lon = selected_location["lon"]
                radius = 500  # Search within 0.5 km radius

                networks_data = get_wifi_networks(lat, lon, radius, api_name, api_token)
                networks = networks_data.get('results', [])
                display_open_networks(networks)

                while True:
                    another_search = input("Do you want to make another search [yes, no]? ").lower()
                    if another_search in ["yes", "y"]:
                        break
                    elif another_search in ["no", "n"]:
                        print("Exiting...")
                        return
                    else:
                        print("Please answer with 'yes' or 'no'.")
        
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()
