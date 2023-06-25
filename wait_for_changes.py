import requests
from time import sleep, time

def wait_for_amp_changes():
    url = "http://192.168.2.203/api/status?filter=amp"
    response = requests.get(url)
    current_value = response.json()['amp']
    num_changes = 0
    start_time = time()

    while num_changes < 2 and time() - start_time < 30:
        sleep(0.5)  # wait for .5 seconds
        response = requests.get(url)
        new_value = response.json()['amp']

        if new_value != current_value:
            num_changes += 1
            print(f"Value changed ({num_changes}/3): {new_value}")
            current_value = new_value

    if num_changes == 2:
        return True
    else:
        return False