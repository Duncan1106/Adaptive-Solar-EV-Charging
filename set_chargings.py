from requests import get

def set_charging(s: int) -> bool:
    """Send a GET request to start or stop charging the EV.

    Args:
        s (str): The status to set for charging. 0 to start charging, 1 to stop charging.

    Returns:
        bool: True if the GET request was successful and the status code is 200, False otherwise.
    """
    set_charging_url = "http://192.168.2.203/api/set?frc="
    r = requests.get(set_charging_url + str(s))
    return r.status_code == 200


# check if script is run as a script
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--s', type=int, help='The status to set for charging. 0 to start charging, 1 to stop charging')
    args = parser.parse_args()
    set_charging(args.set)