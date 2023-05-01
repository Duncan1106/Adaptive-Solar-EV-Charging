from logger import log_info
from set_amps import set_amp
from count_stops import counter
from set_chargings import set_charging
from get_data import get_amp


# Initialize the counter and last called time
counter.count = 0
counter.last_called = None


############################################################################################################
##   ToDo:                                                                                                ##
##         - possible remove and only use adaptive charging when giving the charging_steps as parameter   ##
############################################################################################################

# def max_adaptive_charging(max_charging_power: float, actual_charging_power: float, charging_steps: dict):
#     charging_steps = {6 : 4100, 7 : 4700, 8 : 5400, 9 : 6100, 10 : 6800}
#     charging_amps = 6
#     for amps, power in charging_steps.items():
#         if power <= max_charging_power:
#             charging_amps = amps
#             sleep_time = 4
#         else:
#             sleep_time = 3
#             break
#     if charging_amps != get_amp:
#         set_amp(charging_amps)
#         log_info(f"Charging amps updated to {charging_amps} A")
#     set_charging(0)
#     log_info(f"Charging power: {actual_charging_power} W \nCharging amps: {charging_amps} A")
#     status = f"Available Power: {round (max_charging_power)}W, Amps = {charging_amps}A, Charging: {round (actual_charging_power)}W"
#     return status, sleep_time

def max_charging(pv_power, home_consumption, actual_charging_power):
    # set charging to allow
    set_amp(16)
    set_charging(0)
    sleep_time = 30

    ##########################################################################################################################################################################
    ## ToDo:                                                                                                                                                                ##
    ##      - possible check for 3 phase charging ?!?!                                                                                                                      ##
    ##      - temporaly disable one phase check and allow three phase charging                                                                                              ##
    ##      - maybe add counter that counts the times this got triggered and only after a certain amount changes phases, because phase switching takes about 15-30s         ##
    ##########################################################################################################################################################################
    
    log_status = f"PV Power ({pv_power}W) is larger than Home Consumption ({home_consumption}W) and the charger already charges with max power( {actual_charging_power}W)"
    log_info(log_status)
    return log_status, sleep_time

def adaptive_charging(max_charging_power: float, actual_charging_power: float, charging_steps):
    # Define charging steps in amps and power (in watts)
    charging_steps = {6 : 1300, 7 : 1600, 8 : 1800, 9 : 2000, 10 : 2300, 11 : 2500, 12 : 2700, 13 : 3000, 14 : 3200, 15 : 3400, 16 : 3700}
    # set amps to lowest value possible
    charging_amps = 6
    # set charging to allow
    for amps, power in charging_steps.items():
        if power <= max_charging_power:
            charging_amps = amps
            sleep_time = 4
        else:
            sleep_time = 3
            break

    if charging_amps != get_amp:
        set_amp(charging_amps)
        log_info(f"Charging amps updated to {charging_amps} A")
    set_charging(0)
    log_info(f"Charging power: {actual_charging_power} W \nCharging amps: {charging_amps} A")
    status = f"Available Power: {round (max_charging_power)}W, Amps = {charging_amps}A, Charging: {round (actual_charging_power)}W"
    return status, sleep_time

def slow_charging(amps: int, grid_to_home: float, max_charging_power: float, actual_charging_power: float):
    sleep_time = 5
    set_charging(0)
    set_amp(amps)
    log_status = "Setting amps to 6 to not draw too much power from grid but continue charging"
    log_info(log_status)
    status = f"Grid Power: {round (grid_to_home)}W and PV Power: {round (max_charging_power)}, Amps = 6A, Charging: {round (actual_charging_power)}W"
    return log_status, sleep_time

def no_charging(grid_to_home: float):
    sleep_time = 5
    set_charging(1)
    counter()
    log_status = f"Stopping Charging because too much power is drawn from the grid: {grid_to_home}W"
    log_info(log_status)
    status = f"Grid Power: {round (grid_to_home)}W, Not Charging: 0W"
    return log_status, sleep_time
