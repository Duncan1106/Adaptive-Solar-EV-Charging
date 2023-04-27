from logger import log_info
from set_amps import set_amp
from count_stops import counter
from set_chargings import set_charging


# Initialize the counter and last called time
counter.count = 0
counter.last_called = None

def adaptive_charging(max_charging_power: float, actual_charging_power: float):
    # Define charging steps in amps and power (in watts)
    charging_steps = {6 : 1300, 7 : 1600, 8 : 1800, 9 : 2000, 10 : 2300, 11 : 2500, 12 : 2700, 13 : 3000, 14 : 3200, 15 : 3400, 16 : 3700}
    # set amps to lowest value possible
    charging_amps = 6
    # set charging to allow
    set_charging(0)
    for amps, power in charging_steps.items():
        if power <= max_charging_power:
            charging_amps = amps
            sleep_time = 10
            sleep_str = "10"
        else:
            sleep_str = "08"
            sleep_time = 8
            break
    set_amp(charging_amps)
    log_info(f"Charging power: {actual_charging_power} W \nCharging amps: {charging_amps} A")
    status = f"Available Power: {round (max_charging_power)}W, Amps = {charging_amps}A, Charging: {round (actual_charging_power)}W"
    return status, sleep_time, sleep_str

def slow_charging(amps: int, grid_to_home: float, max_charging_power: float, actual_charging_power: float):
    sleep_time = 10
    sleep_str = "10"
    set_charging(0)
    set_amp(amps)
    log_status = "Setting amps to 6 to not draw too much power from grid but continue charging"
    log_info(log_status)
    status = f"Grid Power: {round (grid_to_home)}W and PV Power: {round (max_charging_power)}, Amps = 6A, Charging: {round (actual_charging_power)}W"
    return log_status, sleep_time, sleep_str

def no_charging(grid_to_home: float):
    sleep_time = 10
    sleep_str= "10"
    set_charging(1)
    counter()
    log_status = f"Stopping Charging because too much power is drawn from the grid: {grid_to_home}W"
    log_info(log_status)
    status = f"Grid Power: {round (grid_to_home)}W, Not Charging: 0W"
    return log_status, sleep_time, sleep_str