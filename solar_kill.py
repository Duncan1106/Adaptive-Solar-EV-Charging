import os
import subprocess
from logger import log_info

def get_pid_from_lockfile(lockfile_name):
    try:
        with open(lockfile_name, 'r') as file:
            pid = int(file.read().strip())
            return pid
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading PID from lockfile: {lockfile_name}. Error: {e}")
        return None

def kill_process_by_lockfile(lockfile_name):
    pid = get_pid_from_lockfile(lockfile_name)
    if pid is not None:
        try:
            # Send the SIGTERM signal to the process using the kill command
            subprocess.run(['kill', str(pid)], check=True)
            print(f"Process with PID {pid} killed for lockfile: {lockfile_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with PID {pid} for lockfile: {lockfile_name}. Error: {e}")
    else:
        print(f"Failed to get the PID from lockfile: {lockfile_name}")

def solar_kill(pv_power):
    """
    Kill the whole script if the sun goes down and not enough solar power is available
    """
    if pv_power < 10:
        log_info(f"Stopping whole script because sun has gone down: {pv_power}W")
        lockfile_path = '/home/pi/pv-charging.lock'
        kill_process_by_lockfile(lockfile_path)
