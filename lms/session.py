import requests
import json
import pprint

from bs4 import BeautifulSoup
from lms import _LOG as log
import lms._settings as settings

try:  # JUST FOR DEBUG
    from __own import Account as acc

except ImportError:
    pass


class GetSession:
    def __init__(self):
        self.session = requests.Session()
        log('debug', 'session.GetSession.__init__', str(id(self.session)))

    def _login(self) -> bool:
        if settings.USER_INFO['usr_id'] is None:     # FOR DEBUG
            settings.USER_INFO['usr_id'] = acc.UID

        if settings.USER_INFO['usr_pwd'] is None:
            settings.USER_INFO['usr_pwd'] = acc.PWD

        log('info', 'session.GetSession.__init__', 'login start')
        res = self.session.post(settings.LOGIN_URL, data=settings.USER_INFO)

        if res.status_code == 200:
            log('info', 'session.GetSession.__init__', 'login success!')
            return True
        else:
            log('info', 'session.GetSession.__init__', 'login failed..')
            return False


if __name__ == "__main__":
    login = GetSession()
    login._login()