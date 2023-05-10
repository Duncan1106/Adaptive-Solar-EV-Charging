from requests import get
from logger import log_error

def get_solar_and_home_data() -> dict:
    """
    Retrieve solar and home energy data from the given API endpoint.

    Args:
        None.

    Returns:
        dict: A dictionary containing the retrieved solar and home energy data.

    Raises:
        requests.exceptions.RequestException: If an error occurs while making the API request.
        requests.exception.Timeout: If the api request times out.
        requests.exception.HTTPError: If any http eroor accures.

    """
    try:
        url = "http://192.168.2.204:8087/getBulk/plenticore.0.devices.local.Pv_P,plenticore.0.devices.local.Home_P,go-e.0.energy.power,plenticore.0.devices.local.HomeGrid_P"
        response = get(url, timeout=10)
        response.raise_for_status()
        data_api = response.json()
        url = "http://192.168.2.203/api/status?filter=nrg"
        response = get(url)
        response.raise_for_status()
        data_car = response.json()
        return data_api, data_car
    except requests.exceptions.Timeout as e:
        log_error(e)
        return None
    except requests.exceptions.HTTPError as e:
        log_error(e)
        return None
    except requests.exceptions.RequestException as e:
        log_error(e)
        return None

def get_phase():
    try:
        url = "http://192.168.2.203/api/status?filter=fsp"
        response = get(url)
        response.raise_for_status()
        data = response.json()
        return data['fsp']
    except requests.exceptions.Timeout as e:
        log_error(e)
        return None
    except requests.exceptions.HTTPError as e:
        log_error(e)
        return None
    except requests.exceptions.RequestException as e:
        log_error(e)
        return None

def get_charging():
    try:
        url = "http://192.168.2.203/api/status?filter=frc"
        response = get(url)
        response.raise_for_status()
        data = response.json()
        return data['frc']
    except requests.exceptions.Timeout as e:
        log_error(e)
        return None
    except requests.exceptions.HTTPError as e:
        log_error(e)
        return None
    except requests.exceptions.RequestException as e:
        log_error(e)
        return None

def get_amp():
    try:
        url = "http://192.168.2.203/api/status?filter=amp"
        response = get(url)
        response.raise_for_status()
        data = response.json()
        return data['amp']
    except requests.exceptions.Timeout as e:
        log_error(e)
        return None
    except requests.exceptions.HTTPError as e:
        log_error(e)
        return None
    except requests.exceptions.RequestException as e:
        log_error(e)
        return None

def retrieve_values():
    """Retrieve values from the API data.

    Returns:
    --------
    Floats
        The retrieved values in the following order:
        - pv_power: float
        - home_consumption: float
        - actual_charging_power: float
        - grid_to_home: float
    """
    api_data, car_data = get_solar_and_home_data() # get the data from api

    pv_power = round (api_data[0]['val'], 5)  # in watts
    home_consumption = round (api_data[1]['val'], 5)  # in watts
    actual_charging_power = round (car_data['nrg'][11]) # in watts
    grid_to_home = round (api_data[3]['val'] ,5) # in watts
    return pv_power, home_consumption, actual_charging_power, grid_to_home


if __name__ == '__main__':
    retrieve_values()