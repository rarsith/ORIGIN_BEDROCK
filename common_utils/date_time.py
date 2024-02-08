from datetime import datetime

class DateTime(object):
    def __init__(self):
        self.time_now = datetime.now()

    @property
    def curr_time(self):
        return self.time_now.strftime("%H:%M")

    @property
    def curr_date(self):
        return self.time_now.strftime("%Y-%m-%d")

