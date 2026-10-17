def format_time(moment, use_24_hour=True):
    if use_24_hour:
        return moment.strftime("%H:%M:%S")
    else:
        return moment.strftime("%I:%M:%S %p")
