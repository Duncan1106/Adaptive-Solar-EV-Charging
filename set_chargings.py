from requests import get
from get_data import get_charging
from count_stops import stops_counter 

stops_counter.count = 0
stops_counter.last_called = None

def set_charging(s: int) -> bool:
    """Send a GET request to start or stop charging the EV.

    Args:
        s (int): The status to set for charging. 0 to start charging, 1 to stop charging.

    Returns:
        str: .
    """
    print (get_charging())
    if get_charging() == s:
        return ""
    else:
        set_charging_url = "http://192.168.2.203/api/set?frc="
        get(set_charging_url + str(s))
        if s == 1:
            stops_counter()
            return "Stopping Charging\n"
        else:
            return "Starting Charging\n"

# check if script is run as a script
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--set', type=int, help='The status to set for charging. 0 to start charging, 1 to stop charging')
    args = parser.parse_args()
    print (set_charging(args.set))