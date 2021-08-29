import requests
import json
import pprint

from bs4 import BeautifulSoup
from lms import _LOG as log
from lms._settings import *

try:  # JUST FOR DEBUG
    from lms._own_info import *

except ImportError:
    pass


class GetSession:
    def __init__(self):
        self.session = requests.Session()
        log('debug', 'session.GetSession.__init__', str(id(self.session)))

    def _login(self) -> bool:
        if USER_INFO['usr_id'] is None:     # FOR DEBUG
            USER_INFO['usr_id'] = USR_ID

        if USER_INFO['usr_pwd'] is None:
            USER_INFO['usr_pwd'] = USR_PW

        log('info', 'session.GetSession.__init__', 'login start')
        res = self.session.post(LOGIN_URL, data=USER_INFO)

        if res.status_code == 200:
            log('info', 'session.GetSession.__init__', 'login success!')
            return True
        else:
            log('info', 'session.GetSession.__init__', 'login failed..')
            return False


if __name__ == "__main__":
    login = GetSession()
    login._login()