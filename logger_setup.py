import logging

def setup_logger(name=None, level=logging.INFO, log_to_file=False, log_file="app.log"):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        if log_to_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)

            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

    return logger

def setup_query_time_logger():
    query_time_logger = logging.getLogger("query_time_logger")
    query_time_logger.setLevel(logging.INFO)

    query_time_handler = logging.FileHandler("query_time.log")
    query_time_handler.setLevel(logging.INFO)

    # Add a formatter to include timestamps
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    query_time_handler.setFormatter(formatter)

    # Add the handler to the logger
    query_time_logger.addHandler(query_time_handler)

    return query_time_logger