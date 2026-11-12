from datetime import datetime

def datetime_timestamp():
    # Get the current date and time
    current_datetime = datetime.now()
    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H%M%S")

    return formatted_datetime
