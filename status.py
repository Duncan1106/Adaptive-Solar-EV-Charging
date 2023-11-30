from time import sleep
from logger import log_info

def status_and_sleep(status_data: str, sleep_str: str, sleep_time: int, status: str) -> None:
    """
    Log the current status, print the sleep duration, and then sleep for the given time.

    Args:
    - status_data (str)): A string containing the status message.
    - sleep_str (str): A string representing the sleep duration in seconds.
    - sleep_time (int): An integer representing the number of seconds to sleep.
    - status (str): A string representing the current status.

    Returns:
    - None
    """
    # Wait for x seconds before running the loop again
    log_info(status_data)
    print(f"Sleeping for {sleep_str} seconds | {status}")
    sleep(sleep_time)
