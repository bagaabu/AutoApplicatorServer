from datetime import datetime


def get_time():
    time_info = datetime.today()
    time_stamp = time_info.timestamp()
    time_str = datetime.strftime(time_info, '%Y-%m-%d %H:%M:%S')
    return time_stamp, time_str
