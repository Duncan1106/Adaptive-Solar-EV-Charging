def calculate_available_power(pv_power, home_consumption, buffer, actual_charging_power) -> float:
    """
    Calculates the available power for charging an electric vehicle based on the input parameters.

    Args:
        pv_power (float): The power produced by the solar panels in watts.
        home_consumption (float): The power consumed by the home appliances in watts.
        buffer (float): The amount of power reserved for other purposes in watts.
        actual_charging_power (float): The actual charging power required by the electric vehicle in kilowatts.

    Returns:
        float: The available power for charging an electric vehicle in watts, rounded to 5 decimal places.
    """
    return round(pv_power - home_consumption - buffer + actual_charging_power, 5)


def check_max_charging_power(available_power) -> float:
    """
    Given the available power, returns the maximum charging power that can be safely used.

    Parameters:
        available_power (float): The power available for charging (in watts).
    Returns:
        float: The maximum charging power that can be safely used (in watts).
    """

    return max(0, available_power)²

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Calcultaes the available power and the maximum charging power available for ev charging.')
    parser.add_argument('-p', '--pv-power', type=float, help='Pv Power produced by the modules')
    parser.add_argument('-h', '--hone-power', type=float, help='home power consumption ')
    parser.add_argument('-b', '--buffer', type=float, help='buffer to be left and untouched when calulating available power')
    parser.add_argument('-b', '--charging_power', type=float, help='Current charging power the ev is charging with')

    args = parser.parse_args()

    availbale_power = calculate_available_power(args.pv-power, args.home-power, args.buffer, args.charging_power)
    check_max_charging_power(available_power)