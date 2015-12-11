import datetime
import errors
import settings
from helpers import formathelp

__author__ = 'Robert Vagt'

class MyDate():
    def __init__(self, date_string):
        #TODO
        self.year = 2000
        self.month = 1
        self.day = 1

    def format_self(self):
        year = str(self.year)
        if self.month <= 9:
            month = "0" + str(self.month)
        else:
            month = str(self.month)
        if self.month <= 9:
            day = "0" + str(self.day)
        else:
            day = str(self.day)
        return year, month, day

    def purino_get(self):
        year, month, day = self.format_self()
        return "{}.{}.{}".format(day, month, year)

    def sql_get(self):
        year, month, day = self.format_self()
        return "{}-{}-{}".format(year, month, day)

def timestamp():
    """
    :return: Timestamp and current username
    """
    now = datetime.datetime.now()
    return "{} - {}.{}.{} {}:{}:{} - ".format(settings.username, now.day, now.month, now.year,
                                             now.hour, now.minute, now.second)


def today():
    """
    :return: Timestamp and current username
    """
    now = datetime.datetime.now()
    return formathelp.format_date("{}.{}.{}".format(now.day, now.month, now.year))



