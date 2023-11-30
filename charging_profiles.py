from logger import log_info
from get_data import get_amp
from set_amps import set_amp
from set_chargings import set_charging

def adaptive_charging(max_charging_power: float, actual_charging_power: float):
    # Define charging steps in amps and power (in watts)
    charging_steps = {6 : 1300, 7 : 1600, 8 : 1800, 9 : 2000, 10 : 2300, 11 : 2500, 12 : 2700, 13 : 3000, 14 : 3200, 15 : 3400, 16 : 3700}
    # set amps to lowest value possible
    charging_amps = 6
    # set charging to allow
    for amps, power in charging_steps.items():
        if power <= max_charging_power:
            charging_amps = amps
            sleep_time = 5
            sleep_str = "05"
        else:
            sleep_str = "05"
            sleep_time = 5
            break

    if charging_amps != get_amp():
        set_amp(charging_amps)
        log_info(f"Charging amps updated to {charging_amps} A")
        log_info(f"Charging power: {actual_charging_power} W")
    set_charging(0)
    status = f"Available Power: {round (max_charging_power)}W, Amps = {charging_amps}A, Charging: {round (actual_charging_power)}W"
    return status, sleep_time, sleep_str

def slow_charging(amps: int, grid_to_home: float, max_charging_power: float, actual_charging_power: float):
    sleep_time = 5
    sleep_str = "05"
    set_amp(amps)
    set_charging(0)
    log_status = "Setting amps to 6 to not draw too much power from grid but continue charging"
    log_info(log_status)
    status = f"Grid Power: {round (grid_to_home)}W and PV Power: {round (max_charging_power)}, Amps = 6A, Charging: {round (actual_charging_power)}W"
    return log_status, sleep_time, sleep_str

def no_charging(grid_to_home: float):
    sleep_time = 4
    sleep_str= "04"
    set_charging(1)
    log_status = f"Stopping Charging because too much power is drawn from the grid: {grid_to_home}W"
    log_info(log_status)
    status = f"Grid Power: {round (grid_to_home)}W, Not Charging: 0W"
    return log_status, sleep_time, sleep_str