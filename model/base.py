from datetime import timedelta, datetime
import jdatetime
from orm.spreadsheet_orm.v1.models  import Entity as BaseEntity
from .configuration import GOOGLE_IAM_ACCOUNT, CURRENT_GMT_TIME_OFFSET


class Entity(BaseEntity):
    _access = GOOGLE_IAM_ACCOUNT
    _time_offset = CURRENT_GMT_TIME_OFFSET


def convertDatetime(s):
    if type(s) in [jdatetime.datetime, datetime]:
        print(1)
        return s

    time_parts = s.replace('T', ' ').split(" ")
    if len(time_parts) == 1:
        time_parts += ["00:00:00"]

    [date, time] = time_parts
    if date.find('-') >= 0:
        [year, month, day] = date.split("-")
    else:
        [month, day, year] = date.split("/")

    offset = None
    if time.find('Z') >= 0:
        [time, offset] = time.split(".")
        [hour, minutes, seconds] = time.split(":")
    elif time.find('.') >= 0:
        [time, _] = time.split(".")
        [hour, minutes, seconds] = time.split(":")
    else:
        offset = False
        [hour, minutes, seconds] = time.split(":")

    t = datetime(
        year=int(year),
        month=int(month),
        day=int(day),
        hour=int(hour),
        minute=int(minutes),
        second=int(seconds)
    )

    if offset:
        t = t + timedelta(minutes=CURRENT_GMT_TIME_OFFSET)
    return t
