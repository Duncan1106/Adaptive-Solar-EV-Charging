from time import sleep
from logger import log_info
from set_amps import set_amp
from set_phases import set_phase
from set_chargings import set_charging
from get_data import get_amp, get_phase

def adaptive_charging(max_charging_power: float, actual_charging_power: float, charging_steps: dict, use_three_phases: bool):
    # set amps to lowest value possible
    charging_amps = 6
    # setting to 3 phase or 1 phase based on use_three_phases
    if use_three_phases:
        log_phase = set_phase(2)
        set_amp(6)
    else:
        log_phase = set_phase(1)

    for amps, power in charging_steps.items():
        if power <= max_charging_power:
            charging_amps = amps
            sleep_time = 5
        else:
            sleep_time = 5
            break
        amp_log = set_amp(charging_amps)
        if amp_log != None:
            log_info(amp_log)

    # allow charging
    log_charging = set_charging(0)
    log_info(f"Amps = {charging_amps} A, Power: {round (actual_charging_power)} W")
    status = f"Available Power: {round (max_charging_power)}W | Amps = {charging_amps} A, Power: {round (actual_charging_power)} W"
    return status, sleep_time, use_three_phases, log_phase, log_charging

def slow_charging(amps: int, grid_to_home: float, max_charging_power: float, actual_charging_power: float):
    set_amp(amps)
    # setting to 1 phase because power isn't enough
    log_phase = set_phase(1)
    log_charging = set_charging(0)
    sleep_time = 4
    log_status = f"Available Power: {round (max_charging_power)}W | Setting to {amps}A to draw not too much power from grid"
    log_info(log_status)
    status = f"Grid Power: {round (grid_to_home)}W, PV Power: {round (max_charging_power)} | Amps = {amps}A, Charging: {round (actual_charging_power)}W"
    return status, sleep_time, False, log_phase, log_charging

def no_charging(available_power: float, fsp: bool):
    if not fsp:
        log_phase = set_phase(1)
    else:
        log_phase = None
    sleep_time = 3
    log_charging = set_charging(1)
    log_status = f"Too little power is available: {available_power + 200 if available_power < 0 else available_power}W"
    log_info(log_status)
    status = f"Available Power: {available_power}W, Not Charging: 0W"
    return status, sleep_time, False, log_phase, log_charging