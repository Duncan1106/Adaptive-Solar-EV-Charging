from time import sleep, time
from set_chargings import set_charging

def counter():
    if counter.last_called is not None and time() - counter.last_called > 300:
        # If it has been more than 5 minutes since the last call, reset the counter
        counter.count = 0
    counter.count += 1  # Increase the counter
    wait_time = 10 + (counter.count) # Calculate the wait time
    sleep(wait_time)  # Wait for the specified time
    counter.last_called = time()  # Update the last called time

    # Call different functions based on the number of calls
    if counter.count == 20:
        print ("Stopped charging 10 times in short time distance, waiting one minute for things to settle down")
        sleep(60)
    elif counter.count == 40:
        print ("Stopped charging 20 times in short time distance, waiting 2 minutes for things to settle down")
        set_charging(1)
        sleep(120)
    return counter.count

if __name__ == '__main__':
    # Initialize the counter and last called time
    counter.count = 0
    counter.last_called = None
    counter()