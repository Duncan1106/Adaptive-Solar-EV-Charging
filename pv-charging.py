#!/usr/bin/python3
# -*- coding:utf-8 -*-

from logger import log_info
from datetime import datetime
from status import status_and_sleep
from check_1_phase import check_1_phase
from modbus_data import return_data_to_script
from get_data import get_charged_energy, get_chip_id
from charging_profiles import adaptive_charging, slow_charging, no_charging
from power_calculations import calculate_available_power, check_max_charging_power

def evaluate_charging_start(grid_to_home: float, max_charging_power: float, actual_charging_power: float, charging_style: int):
    """Evaluate whether to start or stop charging the electric vehicle based on the available power.

    Args:
        - grid_to_home (float): power flow from the grid to home, in watts
        - max_charging_power (float): maximum charging power that can be used for the electric vehicle, in watts
        - actual_charging_power (float): actual charging power being used for the electric vehicle, in watts
        - charging_style (int): the style to charge the ev: aggressive(0) or conservative(1)

    Returns:
        A tuple containing:
        - status (str): a string containing the status of the charging process and the available power, in watts
        - sleep_time (int): duration of time the function should sleep for, in seconds
        - sleep_str (str): a string representation of the sleep time, in the format of mm
    """
    if charging_style == 0:
        grid_to_home_ref = 2000
        amps_slow = 6
    elif charging_style == 1:
        grid_to_home_ref = 800
        amps_slow = 6
    else:
        raise ValueError("The provided charging style is invalid, there are only two style: 0 -> aggressive and 1 -> conservative; default´is conservative")
    if actual_charging_power < 100:
        is_starting_charging = True
    else:
        is_starting_charging = False

    if max_charging_power >= 1200 and grid_to_home <= grid_to_home_ref:
        return adaptive_charging(max_charging_power, actual_charging_power, is_starting_charging)
    if 800 <= max_charging_power < 1200 and grid_to_home < grid_to_home_ref:
        return slow_charging(amps_slow, grid_to_home, max_charging_power, actual_charging_power)
    else:
        return no_charging(grid_to_home)

def loop(buffer: float, style: int)-> None:
    """
    This function retrieves solar and home energy data from an API and then calculates available and maximum charging
    power for an electric vehicle. It then uses this information to either allow or prevent charging of the vehicle and
    sets the appropriate charging current. It also prints the current status of the system and waits for a specified
    amount of time before running the loop again.

    Args:
    - data_url (str): URL of the API that provides solar and home energy data
    - buffer (float): Buffer power in watts that needs to be left available to prevent power cuts or tripping
    - steps (dict): Mapping of different charging currents to their corresponding power requirements

    Returns: None
    """

    while True:
        # Check for 1 phase usage
        check_1_phase()
        pv_power, home_consumption, actual_charging_power, grid_to_home = return_data_to_script()
        charged_energy = get_charged_energy()
        chip_id = get_chip_id()
        available_power = calculate_available_power(pv_power, home_consumption, buffer, actual_charging_power)
        max_charging_power = check_max_charging_power(available_power)

        # style is 0 if chip id 1, elif 1 if chip id 2 else stlye
        style = 0 if chip_id == 1 else (1 if chip_id == 2 else style)

        # only log if style has changed
        if style != style_changed:
            log_info(f"Charging style changed from {style_changed} to {style}")
            style_changed = style

        # Create status message
        #status = f"Status:\n Grid Power to Home: {grid_to_home}W\n Pv Power: {pv_power}W\n Home consumption: {home_consumption}W\n PV Power Available for Grid: {round(pv_power - home_consumption + actual_charging_power, 3)}W\n Available charging power: {available_power}W\n Maximum charging power that can be drawn from the PV:  {max_charging_power}W\n"
        status = f"Grid Power to Home: {grid_to_home}W; Pv Power: {pv_power}W; Home consumption: {home_consumption}W; PV Power Available for Grid: {round(pv_power - home_consumption + actual_charging_power, 3)}W; Available charging power: {available_power}W; Actual charging power: {actual_charging_power}W; Charged Energy: {charged_energy}kWh; Used Chip Id: {chip_id}"

        # Check weather to charge or not based on available grid and pv power
        status_text, sleep_time, sleep_string = evaluate_charging_start(grid_to_home, max_charging_power, actual_charging_power, style)

        # Print the status message and wait for specified amount of time
        status_and_sleep(status, sleep_string, sleep_time, status_text)

def acquire_lock():
    """Create lockfile and write PID"""
    import os
    import sys
    pid = str(os.getpid())
    if os.path.isfile(LOCKFILE):
        with open(LOCKFILE, 'r') as f:
            old_pid = f.read().strip()
        if os.path.exists('/proc/' + old_pid):
            print('Script is already running.')
            sys.exit()
        else:
            os.remove(LOCKFILE)
    with open(LOCKFILE, 'w') as f:
        f.write(pid)

def main(buffer_power, style) -> None:
    """
    The main function that runs the loop for the EV charger.

    Args:
        buffer_power: the power that shoulkd remain untouched and not be used for ev charging, that shoukld be available for other home consumers
        style: the style in what the ev shoulld get charged, more aggressive, should result in fewer stops, but potentialy more power drawn from grid, more conservative, should result in more stops, but nearly no power draw from grid

    Returns:
        None
    """

    chip_id = get_chip_id()
    style =  0 if chip_id == 1 else (1 if chip_id == 2 else style)
    style_changed = style

    start = f"Startin1g PV Surplus EV charging, buffer power: {buffer_power}W, charging style: {'aggressive' if style == 0 else 'conservative'}"
    if check_1_phase(True):
        print (start)
        log_info(start)
        loop(buffer_power, style)

# check if script is run as a script
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--buffer', type=int, default=200, help='the power that should be left of the PV power for the home and should not be drawn for ev charging, default is 200W')
    parser.add_argument('--style', type=int, default=1,help='should the algorithm be more aggressive (0) or more conservative (1) in charging the ev aggressive should result in fewer stops, but potencial draw from gird, conservative should stop more often and will try to not draw any power from grid')
    args = parser.parse_args()

    LOCKFILE = '/home/pi/pv-charging.lock'
    acquire_lock()
    main(args.buffer, args.style)
