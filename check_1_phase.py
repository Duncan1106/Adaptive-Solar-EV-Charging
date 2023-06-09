import sys ### possibly not needed
from time import sleep
from requests import get
from logger import configure_logging
from user_kill import user_input_kill
from set_chargings import set_charging
from progress_bar import run_progress_bar
from wait_for_changes import wait_for_amp_changes

def check_1_phase(first_check: bool = False, use_three_phases: bool = False) -> bool:
    """Checks if one phase is being used for charging.

    Args:
        first_check (bool): Flag to indicate if this is the first check.
            Defaults to False.
        use_three_phases (bool): Flag to indicate if the systems has enough solar power for three phase charging
            Default to False.

    Returns:
        bool: Returns True if one phase is being used for charging.
    """

    # URL for checking if one phase is used
    check_1_phase_url = "http://192.168.2.203/api/status?filter=fsp"

    while True:
        # Get the value of fsp from the API
        fsp = get(check_1_phase_url).json()['fsp']
        if first_check:
            configure_logging()
            run_progress_bar()
        if fsp:
            return True
        if not fsp:
            if use_three_phases:
                return True
            # If this is the first check and three phases are being used, wait for one phase to be used
            if wait_for_amp_changes():
                # If amps have changed three times indicate the user the pv-charging will stop and start charging
                user_input_kill()
                sys.exit()  ################### replace with suitable wait loop for changes in phases or something like this ###################
            # if amps hasnt chanegd three times, stop charging and wait for one phase to be used
            set_charging(1)
        sleep(30)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='checks if one phase is used and only return if 1 phase is used')
    parser.add_argument('-fc', '--firstCheck', type=bool, default=False, help='is it run the first time or not')
    args = parser.parse_args()
    check_1_phase(args.firstCheck)