from time import sleep
from set_amps import set_amp

# user input signal that indicates script wont interrupt anymore
def user_input_kill() -> None:
    """
    This function sets the charging amps to two different values to indicate to the user that input was received.
    """
    set_amp(6)
    sleep(2)
    set_amp(10)
    sleep(2)
    set_amp(16)
    sleep(2)