from time import sleep, time
from set_phases import set_phase

def counter():
    if counter.last_called is not None and time() - counter.last_called > 120:
        # If it has been more than 5 minutes since the last call, reset the counter
        counter.count = 0
    counter.count += 1  # Increase the counter
    #wait_time = 10 + (counter.count) # Calculate the wait time
    #sleep(wait_time)  # Wait for the specified time
    counter.last_called = time()  # Update the last called time

    # Call different functions based on the number of calls
    if counter.count == 5:
        print ("Changed phases 5 times in a 2 minute periode distance, waiting one minute for things to settle down")
        sleep(60)
    elif counter.count == 10:
        print ("Stopped charging 10 times in a 2 minute periode, waiting 2 minutes for things to settle down")
        sleep(120)
    return counter.count


if __name__ == '__main__':
    # Initialize the counter and last called time
    counter.count = 0
    counter.last_called = None
    counter()