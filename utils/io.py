import os
from datetime import datetime

from enum import IntEnum, unique
from functools import reduce
from random import randint, shuffle

@unique
class FreqType(IntEnum):
    Month = 0
    Week = 1
    Day = 2
    Hour = 3
    Minute = 4
    Second = 5

BASE_OF_TIME = [30, 7, 24, 60, 60]

class DatetimeConverter:
    def __init__(self, formatter: str = '%Y-%m-%d') -> None:
        self.formatter = formatter

    def str2date(self, str_date: str) -> datetime:
        return datetime.strptime(str_date, self.formatter) 

    def date2str(self, date: datetime):
        return date.strftime(self.formatter)

def get_freq_rate(source_freq: FreqType, target_freq: FreqType) -> int:
    return reduce(lambda x, y: x*y, BASE_OF_TIME[source_freq:target_freq])

def create_dir_not_exists(*dirs):
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def get_list_by_sum(total: int, num: int)->list:
    pieces = []
    for idx in range(num-1):
        pieces.append(randint(1,total-sum(pieces)-num+idx))
    pieces.append(total-sum(pieces))
    shuffle(pieces)
    return pieces

def long_predict():
    pass