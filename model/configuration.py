from datetime import datetime

import jdatetime
import pytz

CURRENT_GMT_TIME_OFFSET = 270
TEHRAN_ZONE = pytz.timezone('Asia/Tehran')
NOW = jdatetime.datetime.now()
NOW_GMT = datetime.now()

OFFICIAL_YEAR_DAYS = 366 if NOW.isleap() else 365

GOOGLE_IAM_ACCOUNT = {
        "type": "service_account",
        "project_id": "profile-harvester",
        "private_key_id": "45dd10ea0133b0e7eb3f88010b6493c3b8a330cb",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDYUWs2vUvgOdgd"
                       "\nc1z1Amhq4gR/YsKyZVJWu2/DfHYUwSRq4KsqwXusA3UK0IBINd8INU1VBWzNO6Fn\nGBtGdHQ0u4eWDsVCadQ+zC"
                       "/gEgrxCMGW9q+u6D+/XmKw19k5PojcVVFUVqHqqrMa\nfFi9RHP2DKpjGMsrcikvvZ2H8ZtnW"
                       "+dFPc0wVtLWBbrZXgROIgL5Q5D4SFUfJPwq"
                       "\nalWM94i4dHayasgKEwohcLDmHzKXhuKK1uVNkeIt20wyOysUMflYeMMfJLBgNrpO"
                       "\ncN4Ki4xR3t8oGvItzspeTigk0rE7OQ/e6HzNcxRutKT1NME6VFrAzEkEbZ0CyUCw\nVF3XRaW"
                       "/AgMBAAECggEAE6JGm7zp8O71h+Bh5MMhL+i8nvgbbKgrPwzbahNKTG8m"
                       "\nm3GYJG6HVE33OgVB5eWUQGFGJM9nPrS8EGigISPBk5lQOlu0DJq6bv2HFhlmvaK3\nBexbqc54USnp"
                       "+NvxyKZXM1hzF1D9q7HVEjRZgZd/xvdpuuQUAykYRk/TLcGaNb+q\nkcGuhDbi1euueOLpSK/q4tahQkaNE/rLic9rNcZtT"
                       "+heWhc9nBjGlex8JG5p7Adh\nFnljNeoTtqq2B9s90Du9CyiFvjWAhLxcjAc8i6pWf7NtgBeJazYL0RUAsFWNerzZ"
                       "\nWCYRcWwNDpVIlqxiA6BAS5nQ5sZI8+fbne0k0M/9QQKBgQDzhaNNEHCfWW8mzTLa"
                       "\nh60Ugxg52MeZjbgiedlpWb6xPenofySK9BAfRs804cWoZ5EizvruzOrGY6j7KU/c"
                       "\nsI00QN4TrH4CztzPzkQB4y3lCIM69R3P/gtClMAET8gg85TWmApc+M3D9e9W1fHy"
                       "\nJsCg6bQn7tHQdbmDBHwSel4MkQKBgQDjZu/bQ4Zj9og9H4ti15FwsVtqtXfpgi2t"
                       "\nBqIGTEAproa0lifvt5bdnsfjOz2jAlYsEoPNfiK56M2h0PfetJ+ryEwqKEOt5t7Y"
                       "\nL0aAnmbobORt8R13dAsMOSPiJvSoQ8EJopzqVQDTCQhXKWSfmRDUIimvECtY170L"
                       "\ndOWwnyn1TwKBgQCfObr7sYsh9dUidrsQffPiXJEjiaWAtlQ2XpuUMbToqQXfGfrn\nzAsamC71ccXOheE09EbIiz3a9"
                       "+DOUEXCk8HP77YFARzncyCX01NONJ+WiIldrFWQ\n4Je2MhKW/x9oxDuGUKU+AwRvY8fZbEwlO8dpr0U3cwTHG6JvkygY4N"
                       "/LsQKBgFfr\nIm0JjFn1pPLM0V0jrw185LU69+OF+xbca6Q3ss7qtRX4v/QEbQW+L9YAv3HYo2xi"
                       "\ntCasz8xE38viORMXjmwiAqCB9Li1fA7lKELt+yd9gkunXxch/Gt7ZA45tXmgyG9r\nOXO37Zup8FmSnV6"
                       "/FSyPEMKoY7nznxlg1rUUtGotAoGAaE3KqD1qbswxR3+jy8pw\nZzk+kTadd4m90ZbrEx9feT"
                       "/iHLgkqNp0C9PWr4z1QHzz1NmIdywcQKX2AOoTsfJt\ngE5eCbb8d9y2jyI6Y7cDivyEJ1"
                       "+Ok0mlsGBcFBOc1YHJb2UcGfPFuYlYGHJvNhJZ\nUVtapFNeoSI5mrcLqOjSgps=\n-----END PRIVATE KEY-----\n",
        "client_email": "profile-harvester@profile-harvester.iam.gserviceaccount.com",
        "client_id": "100923802003993761586",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/profile-harvester%40profile-harvester.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

# Sheets
PICTURE_SHEET = "1H9ZnJWwjxZtkTrkNrOQw8XZLrDa29qbEeAjBA7K_weI"
ERROR_SHEET = "1H9ZnJWwjxZtkTrkNrOQw8XZLrDa29qbEeAjBA7K_weI"
LOG_SHEET = "1H9ZnJWwjxZtkTrkNrOQw8XZLrDa29qbEeAjBA7K_weI"

# Address
HOST = ""
local = "http://127.0.0.1:8000"

#Token
token = "ksgjnjew;aldsmksmflsdkekfmv654ef58wf4sa5efdd5fs1"




