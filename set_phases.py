from time import sleep
from requests import get
from get_data import get_phase
from count_phase_changes import phase_counter

phase_counter.count = 0
phase_counter.last_called = None

def set_phase(s: int) -> bool:
    """Send a GET request to start or stop charging the EV.

    Args:
        s (int): The phasses to use for charging. 1 for one phase charging, 2 for 3 phase charging.

    Returns:
        bool: True if the GET request was successful and the status code is 200, False otherwise.
    """
    set_phase_url = "http://192.168.2.203/api/set?psm="
    phase = get_phase()

    if phase and s == 1:
        return None
    elif phase and s == 2:
        phase_counter()
        get(set_phase_url + str(s))
        sleep (20)
        return "\n Setting to 3 phases \n"
    elif not phase and s == 1:
        phase_counter()
        get(set_phase_url + str(s))
        sleep (20)
        return "\n Setting to 1 phase \n"
    elif not phase and s == 2:
        return None
    # r = get(set_phase_url + str(s))
    # sleep (20)
    # return r.status_code == 200

# check if script is run as a script
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--set', type=int, help='The phasses to use for charging. 1 for one phase charging, 2 for 3 phase charging.')
    args = parser.parse_args()
    print (set_phase(args.set))