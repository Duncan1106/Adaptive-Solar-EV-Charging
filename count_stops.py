from time import sleep, time

def stops_counter():
    if stops_counter.last_called is not None and time() - stops_counter.last_called > 120:
        # If it has been more than 5 minutes since the last call, reset the counter
        stops_counter.count = 0
    stops_counter.count += 1  # Increase the counter
    #wait_time = (counter.count)
    #sleep(wait_time)  # Wait for the specified time
    stops_counter.last_called = time()  # Update the last called time

    # Call different functions based on the number of calls
    if stops_counter.count == 20:
        print ("Stopped charging 20 times in short time distance, waiting one minute for things to settle down")
        sleep(60)
    elif stops_counter.count == 40:
        print ("Stopped charging 40 times in short time distance, waiting 2 minutes for things to settle down")
        sleep(120)
    return stops_counter.count


if __name__ == '__main__':
    # Initialize the counter and last called time
    stops_counter.count = 0
    stops_counter.last_called = None
    stops_counter()