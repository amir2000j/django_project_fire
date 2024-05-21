
from .base import *
from .configuration import *


class Picture(Entity):
    _sheet = PICTURE_SHEET
    _table = 'picture'
    _range = ('A', 2, 'E')

    create_date = ''
    id = ''
    status = ''
    picture = ''


    def initialize(self, data):
        super().initialize(data)

        try:
            self.create_date = convertDatetime(self.create_date)
        except ValueError:
            pass


class Error(Entity):
    _sheet = ERROR_SHEET
    _table = 'error'
    _range = ('A', 2, 'D')

    creat_data = ''
    id = ''

    def initialize(self, data):
        super().initialize(data)

        try:
            self.create_date = convertDatetime(self.create_date)
        except ValueError:
            pass

class Log(Entity):
    _sheet = LOG_SHEET
    _table = 'log'
    _range = ('A', 2, 'G')

    create_date = ''
    id = ''
    method = ''
    client = ''
    ip = ''
    address = ''

    def initialize(self, data):
        super().initialize(data)

        try:
            self.create_date = convertDatetime(self.create_date)
        except ValueError:
            pass
