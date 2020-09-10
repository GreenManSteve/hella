import datetime

class Base:
    def __init__(self):
        pass

    def get_time_stamp(self):
        now = datetime.datetime.now()
        return now
