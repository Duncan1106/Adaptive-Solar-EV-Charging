from logger import log_info
from set_amps import set_amp
from get_data import get_amp, get_phase
from count_stops import counter
from set_phases import set_phase
from set_chargings import set_charging
from time import sleep
from count_phase_changes import counter as counter2

# Initialize the counter and last called time
counter.count = 0
counter.last_called = None

counter2.count = 0
counter2.last_called = None

#     ##########################################################################################################################################################################
#     ## ToDo:                                                                                                                                                                ##
#     ##      (-) possible check for 3 phase charging ?!?!                                                                                                                    ##
#     ##      (-) temporaly disable one phase check and allow three phase charging                                                                                            ##
#     ##       -  maybe add counter that counts the times this got triggered and only after a certain amount changes phases, because phase switching takes about 15-30s       ##
#     ##########################################################################################################################################################################

def adaptive_charging(max_charging_power: float, actual_charging_power: float, charging_steps: dict, use_three_phases: bool):
    # set amps to lowest value possible
    charging_amps = 6
    # setting to 3 phase or 1 phase based on use_three_phases
    if use_three_phases:
        if get_phase():
            log = "\n Setting to 3 phases\n"
            print (log)
            log_info(log)
            set_phase(2)
            counter2()
            sleep(20)
    else:
        if not get_phase():
            log = "\n Setting to 1 phase\n"
            print (log)
            log_info(log)
            counter2()
            set_phase(1)
            sleep(20)

    for amps, power in charging_steps.items():
        if power <= max_charging_power:
            charging_amps = amps
            sleep_time = 5
        else:
            sleep_time = 5
            break

    if charging_amps != get_amp():
        set_amp(charging_amps)
        log_info(f"Charging amps updated to {charging_amps} A")
    # allow charging
    set_charging(0)
    log_info(f"Charging power: {actual_charging_power} W\nCharging amps: {charging_amps} A")
    status = f"Available Power: {round (max_charging_power)} W, Amps = {charging_amps} A, Charging: {round (actual_charging_power)} W"
    return status, sleep_time, use_three_phases

def slow_charging(amps: int, grid_to_home: float, max_charging_power: float, actual_charging_power: float):
    # setting to 1 phase because power isn't enough
    if not get_phase():
        set_phase(1)
    sleep_time = 4
    set_amp(amps)
    set_charging(0)
    log_status = "Setting amps to 6 to not draw too much power from grid but continue charging"
    log_info(log_status)
    status = f"Grid Power: {round (grid_to_home)}W and PV Power: {round (max_charging_power)}, Amps = 6A, Charging: {round (actual_charging_power)}W"
    return log_status, sleep_time, False

def no_charging(grid_to_home: float):
    if not get_phase():
        # resetting phase to 1 phase when stopping charging
        set_phase(1)
    sleep_time = 3
    set_charging(1)
    counter()
    log_status = f"Stopping Charging because too much power is drawn from the grid: {grid_to_home}W"
    log_info(log_status)
    status = f"Grid Power: {round (grid_to_home)}W, Not Charging: 0W"
    return log_status, sleep_time, False