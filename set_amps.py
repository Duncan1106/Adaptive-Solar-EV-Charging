from requests import get

def set_amp(amps: int) -> bool:
    """
    Sets the charging amps for a home charger via a given URL.

    Args:
    amps (int): The desired charging amperage, in a range from 6 to 16.

    Returns:
    bool: Returns True if the request was successful (i.e. status code 200), otherwise False.
    """
    if amps < 6 or amps > 16:
        raise ValueError("Desired amperage must be between 6 and 16")
        return None
    set_amps_url = "http://192.168.2.203/api/set?amp="
    r = get(set_amps_url + str(amps))
    return r.status_code == 200

# check if script is run as a script
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--amps', type=int, choices=range(6, 17), help='amp range between 6 and 16 (inclusive)')
    args = parser.parse_args()
    amps = args.amps

    set_amp(amp