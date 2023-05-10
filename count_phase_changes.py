from time import sleep, time

def phase_counter():
    if phase_counter.last_called is not None and time() - phase_counter.last_called > 120:
        # If it has been more than 5 minutes since the last call, reset the counter
        phase_counter.count = 0
    phase_counter.count += 1  # Increase the counter
    #wait_time = 10 + (counter.count) # Calculate the wait time
    #sleep(wait_time)  # Wait for the specified time
    phase_counter.last_called = time()  # Update the last called time

    # Call different functions based on the number of calls
    if phase_counter.count == 5:
        print ("Changed phases 5 times in a 2 minute periode distance, waiting one minute for things to settle down")
        sleep(60)
    elif phase_counter.count == 10:
        print ("changed phases 10 times in a 2 minute periode, waiting 2 minutes for things to settle down")
        sleep(120)
    return phase_counter.count


if __name__ == '__main__':
    # Initialize the counter and last called time
    phase_counter.count = 0
    phase_counter.last_called = None
    print (phase_counter())