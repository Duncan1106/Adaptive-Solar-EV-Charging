import logging
from datetime import datetime, date

def configure_logging(log_level: str = 'INFO'):
    """
    Configures the logging for the application.

    Args:
        log_level (str): The level of logging to use. The options are 'DEBUG', 'INFO',
        'WARNING', 'ERROR', and 'CRITICAL'. The default is 'INFO'.
    """
    logging.basicConfig(filename=f"charging-data_{date.today().strftime('%d-%m-%Y')}.log", level=log_level,
                        format='%(asctime)s %(levelname)s %(message)s')

    start = '''
                     _____    ______  __        __     ______
            /\      / ____|  |  ____| \ \      / /    / _____|
           /  \    | (___    | |__     \ \    / /    / /
          / /\ \    \___ \   |  __|     \ \  / /    |  |
         / ____ \   ____) |  | |____     \ \/ /      \  \____
        /_/    \_\ |______/  |______|     \__/        \______|
                Adaptive Solar EV Charging v.9.0 '''
    print (start)
    log_info (start)
def log_error(message: Exception) -> None:
    """
    Logs an Exception.

    Args:
        message (Exception): The Exception to log.

    Returns:
        None
    """
    logging.exception(message)

def log_info(message: str):
    """
    Logs an informational message with the given logger.

    Args:
        message (str): The message to log.

    Returns:
        None
    """
    logging.info(message)