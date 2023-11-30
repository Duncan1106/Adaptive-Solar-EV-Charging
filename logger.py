import logging
import datetime

def configure_logging(log_level: str = 'INFO'):
    """
    Configures the logging for the application.

    Args:
        log_level (str): The level of logging to use. The options are 'DEBUG', 'INFO',
        'WARNING', 'ERROR', and 'CRITICAL'. The default is 'INFO'.
    """
    logging.basicConfig(filename=f"charging-data_{datetime.date.today().strftime('%d-%m-%Y')}.log", level=log_level, format='%(asctime)s %(levelname)s %(message)s')
    #logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)s %(message)s')

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

