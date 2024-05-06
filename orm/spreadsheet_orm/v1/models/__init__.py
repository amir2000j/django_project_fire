from datetime import datetime, timedelta
from time import sleep

import gspread
import hashlib
from gspread.exceptions import APIError
from traceback_with_variables import iter_exc_lines

SPREADSHEETS_GENERAL_FIELDS = {
    'credentials': 'GOOGLE_INVALID_CREDENTIALS',
    'spreadsheet_id': 'GOOGLE_INVALID_SPREADSHEET_ID',
}

SPREADSHEETS_FIELDS__APPEND_TO_SHEET = {
    **SPREADSHEETS_GENERAL_FIELDS, **{
        'range': 'GOOGLE_INVALID_SPREADSHEET_RANGE',
        'rows': 'GOOGLE_INVALID_SPREADSHEET_DATA',
    }
}

SPREADSHEETS_FIELDS__LOAD_RANGE = {
    **SPREADSHEETS_GENERAL_FIELDS, **{
        'range': 'GOOGLE_INVALID_SPREADSHEET_RANGE',
    }
}

SPREADSHEETS_FIELDS__UPDATE_RANGE = {
    **SPREADSHEETS_GENERAL_FIELDS, **{
        'range': 'GOOGLE_INVALID_SPREADSHEET_RANGE',
        'rows': 'GOOGLE_INVALID_SPREADSHEET_DATA',
    }
}

SPREADSHEETS_SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

build_caches = {}
entity_cache = {}


def spreadsheet(body):
    checksum = hashlib.md5(str(body['credentials']).encode()).hexdigest() + body['spreadsheet_id']
    if checksum in build_caches.keys():
        return 200, build_caches[checksum]

    gc = gspread.service_account_from_dict(body['credentials'], scopes=SPREADSHEETS_SCOPES)
    try:
        build_caches[checksum] = gc.open_by_key(body['spreadsheet_id'])
        return 200, build_caches[checksum]

    except APIError:
        sleep(60)
        return spreadsheet(body)

    except Exception as e:
        return 500, {
            'status': 'failed',
            'error': str(e),
            'details': '\n'.join(list(iter_exc_lines(e)))
        }


class Entity:
    _VALID_TYPES = [str, int, float, datetime]
    _found = False

    _table = None
    _sheet = None
    _range = None
    _access = None
    _time_offset = None

    key = None

    def load(self, tries=10):
        if self._table in entity_cache.keys():
            if self.key in entity_cache[self._table].keys():
                self._found = True
                self.initialize(entity_cache[self._table][self.key])

            return

        status, sheet = spreadsheet({
            "credentials": self._access,
            "spreadsheet_id": self._sheet,
        })

        if status != 200:
            if tries <= 0:
                print("spreadsheet load error", status, sheet)
                raise Exception

            sleep(30)
            return self.load(tries=tries - 1)

        if self._table not in entity_cache.keys():
            entity_cache[self._table] = {}

        try:
            worksheet = sheet.worksheet(self._table)
            for row in worksheet.get_all_values()[1:]:
                if len(row) == 0:  # empty row in sheets
                    continue

                entity_cache[self._table][row[0]] = row

                if row[0] == self.key:
                    self._found = True
                    self.initialize(row)
        except Exception as e:
            if tries <= 0:
                print("spreadsheet load error", e, status, sheet)
                raise Exception

            sleep(30)
            return self.load(tries=tries - 1)

    def save(self, tries=10):
        [start_col, start_row, end_col, _] = self.get_range()
        status, sheet = spreadsheet({
            "credentials": self._access,
            "spreadsheet_id": self._sheet,
        })

        if status != 200:
            if tries <= 0:
                print("spreadsheet load error", status, sheet)
                raise Exception

            sleep(30)
            return self.save(tries=tries - 1)

        try:
            worksheet = sheet.worksheet(self._table)
        except Exception as e:
            if tries <= 0:
                print("spreadsheet load error 2", status, sheet, e)
                raise Exception

            sleep(30)
            return self.save(tries=tries - 1)

        data = [self.key]
        for attr in self.__class__.__dict__:
            if attr[:1] != '_':
                v = getattr(self, attr)
                if type(v) in Entity._VALID_TYPES:
                    if attr.endswith('_date'):
                        try:
                            if type(v) is datetime:
                                v = str(v)

                            if v.find('T') >= 0:
                                v = datetime.fromisoformat(v[:-5]) + timedelta(minutes=self._time_offset)
                                v = str(v)
                                setattr(self, attr, v)
                        except (ValueError, AttributeError) as _:
                            pass

                    data.append(v)

        overwrite = None
        try:
            rows = worksheet.get_all_values()[1:]
            for i in range(0, len(rows)):
                row = rows[i]
                if len(row) == 0:  # empty row in sheets
                    continue

                if row[0] == self.key:
                    overwrite = i

                if self._table not in entity_cache.keys():
                    entity_cache[self._table] = {}

                entity_cache[self._table][row[0]] = row
        except Exception as e:
            if tries <= 0:
                print("S1 overwrite preload error", e)
                raise Exception

            sleep(30)
            return self.save(tries=tries - 1)

        save_response = None
        if overwrite is not None:
            try:
                save_response = worksheet.update(
                    f"{start_col}{start_row + overwrite}:{end_col}{start_row + overwrite}",
                    [data],
                    value_input_option='USER_ENTERED'
                )
                if 'code' in save_response.keys() and save_response['code'] == 429:
                    if tries <= 0:
                        print("S1", save_response)
                        raise Exception

                    sleep(30)
                    return self.save(tries=tries - 1)

                # if save_response['updates']['updatedRows'] == 0:
                #     raise Exception

            except APIError as e:
                print("overwrite spreadsheet save error", save_response, self._table, e, data)
                if tries <= 0:
                    print("S1", save_response)
                    raise Exception

                sleep(30)
                return self.save(tries=tries - 1)
        else:
            try:
                save_response = worksheet.append_rows([data], value_input_option='USER_ENTERED')
                if 'code' in save_response.keys() and save_response['code'] == 429:
                    if tries <= 0:
                        print("S2", save_response)
                        raise Exception

                    sleep(30)
                    return self.save(tries=tries - 1)

            except Exception as e:
                print("new write spreadsheet save error", self._table, data, save_response, e)

        if self._table not in entity_cache.keys():
            entity_cache[self._table] = {}

        entity_cache[self._table][self.key] = data

        self._found = True

        return True

    @classmethod
    def bulky_insert(cls, objects, tries=10):
        [start_col, start_row, end_col, _] = cls.get_range()
        status, sheet = spreadsheet({
            "credentials": cls._access,
            "spreadsheet_id": cls._sheet,
        })

        if status != 200:
            if tries <= 0:
                print("spreadsheet load error", status, sheet)
                raise Exception

            sleep(30)
            return cls.bulky_insert(objects, tries=tries - 1)

        try:
            worksheet = sheet.worksheet(cls._table)
        except Exception as e:
            if tries <= 0:
                print("spreadsheet load error 2", status, sheet, e)
                raise Exception

            sleep(30)
            return cls.bulky_insert(objects, tries=tries - 1)

        do_bulky = []
        do_one_to_one = []
        for obj in objects:
            if obj.found():
                do_one_to_one.append(obj)
                continue

            data = [obj.key]
            for attr in obj.__class__.__dict__:
                if attr[:1] != '_':
                    v = getattr(obj, attr)
                    if type(v) in Entity._VALID_TYPES:
                        if attr.endswith('_date'):
                            try:
                                if type(v) is datetime:
                                    v = str(v)

                                if v.find('T') >= 0:
                                    v = datetime.fromisoformat(v[:-5]) + timedelta(minutes=cls._time_offset)
                                    v = str(v)
                                    setattr(obj, attr, v)
                            except (ValueError, AttributeError) as _:
                                pass

                        data.append(v)

            do_bulky.append(data)

            if cls._table not in entity_cache.keys():
                entity_cache[cls._table] = {}

            entity_cache[cls._table][data[0]] = data

        save_response = None
        try:
            save_response = worksheet.append_rows(
                do_bulky,
                value_input_option='USER_ENTERED'
            )
            if 'code' in save_response.keys() and save_response['code'] == 429:
                if tries <= 0:
                    print("S1", save_response)
                    raise Exception

                sleep(30)
                return cls.bulky_insert(objects, tries=tries - 1)

        except APIError as e:
            print("overwrite spreadsheet save error", save_response, cls._table, e, objects)
            if tries <= 0:
                print("S1", save_response)
                raise Exception

            sleep(30)
            return cls.bulky_insert(objects, tries=tries - 1)

        for item in do_one_to_one:
            item.save()

        return True

    @classmethod
    def check_cache(cls, pk):
        try:
            return pk in entity_cache[cls._table].keys()
        except KeyError as _:
            return False

    def initialize(self, data):
        fields = ['key'] + [
            i for i in self.__class__.__dict__ if i[:1] != '_' and type(getattr(self, i) in Entity._VALID_TYPES)
        ]

        for i in range(0, len(data)):
            setattr(self, fields[i], data[i])

    def __init__(self, key=None):
        self.key = key

        if key and key != '':
            self.load()

    def __str__(self):
        return f"<{type(self).__name__}: #{self.key}>"

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, i):
        return getattr(self, i)

    def found(self):
        return self._found

    def delete(self, tries=10):
        status, sheet = spreadsheet({
            "credentials": self._access,
            "spreadsheet_id": self._sheet,
        })

        if status != 200:
            if tries <= 0:
                print(f"spreadsheet delete {self._table} {self.key}", status, sheet)
                raise Exception

            sleep(30)
            return self.delete(tries=tries - 1)

        try:
            worksheet = sheet.worksheet(self._table)
            row_index = 0
            for row in worksheet.get_all_values():
                row_index += 1
                if len(row) == 0:  # empty row in sheets
                    continue

                if row[0] == self.key:
                    break
        except APIError:
            if tries <= 0:
                print(f"spreadsheet delete {self._table} {self.key}", status, sheet)
                raise Exception

            sleep(30)
            return self.delete(tries=tries - 1)

        try:
            worksheet.delete_rows(row_index)
        except Exception as e:
            print(e)

        self.delete_from_cache()

    def delete_from_cache(self):
        try:
            del entity_cache[self._table][self.key]
        except KeyError:
            pass

    @classmethod
    def clear_cache(cls):
        try:
            del entity_cache[cls._table]
        except KeyError:
            pass

    @classmethod
    def clear_link(cls):
        checksum = hashlib.md5(str(cls._access).encode()).hexdigest() + cls._sheet
        try:
            del build_caches[checksum]
        except KeyError:
            pass

    @classmethod
    def A(cls, filter_check=None, tries=10):
        status, sheet = spreadsheet({
            "credentials": cls._access,
            "spreadsheet_id": cls._sheet,
        })

        if cls._table in entity_cache.keys():
            if len(entity_cache[cls._table].keys()) > 0:
                results = []
                for row in entity_cache[cls._table].values():
                    obj = cls()
                    obj.initialize(row)

                    if filter_check:
                        if not filter_check(obj):
                            continue

                    results.append(obj)
                return results

        if status != 200:
            if tries <= 0:
                print("spreadsheet A error", status, sheet)
                raise Exception

            return cls.A(tries=tries - 1, filter_check=filter_check)

        try:
            worksheet = sheet.worksheet(cls._table)
        except APIError:
            return cls.A(tries=tries - 1, filter_check=filter_check)

        if cls._table not in entity_cache.keys():
            entity_cache[cls._table] = {}

        results = []
        try:
            q = 1
            for row in worksheet.get_all_values()[1:]:
                q += 1
                if len(row) == 0:
                    continue

                obj = cls()
                obj.initialize(row)

                entity_cache[cls._table][obj.key] = row

                if filter_check:
                    if not filter_check(obj):
                        continue

                results.append(obj)
        except APIError:
            return cls.A(tries=tries - 1, filter_check=filter_check)
        except Exception as e:
            print(f"Load Entity.A() Error for {cls._table}", e)

        return results

    @classmethod
    def f(cls, filter_check=None):
        return cls.A(filter_check)

    @classmethod
    def get_range(cls):
        if len(cls._range) == 4:
            [start_col, start_row, end_col, end_row] = cls._range
        elif len(cls._range) == 3:
            [start_col, start_row, end_col] = cls._range
            end_row = ''
        else:
            raise Exception

        return [start_col, start_row, end_col, end_row]

    @classmethod
    def add(cls, row=None, tries=10):
        if row is None:
            row = []

        return cls.bulky_add([row], tries=tries)

    @classmethod
    def bulky_add(cls, rows=None, tries=10):
        if rows is None:
            rows = []

        status, sheet = spreadsheet({
            "credentials": cls._access,
            "spreadsheet_id": cls._sheet,
        })

        if status != 200:
            if tries <= 0:
                print("spreadsheet log bulky add error 1", status, sheet)
                raise Exception

            sleep(30)
            return cls.bulky_add(rows, tries=tries - 1)

        worksheet = sheet.worksheet(cls._table)

        save_response = None
        try:
            save_response = worksheet.append_rows(rows, value_input_option='USER_ENTERED')
            if cls._table not in entity_cache.keys():
                entity_cache[cls._table] = {}

            for row in rows:
                entity_cache[cls._table][row[0]] = row

        except Exception as e:
            if tries <= 0:
                print("spreadsheet log bulky add error 2", save_response, e)
                raise Exception

            sleep(30)
            return cls.bulky_add(rows, tries=tries - 1)

        cls.clear_cache()
