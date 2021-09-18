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
        log('debug', 'session.GetSession.__init__', f'SESSION ID : {str(id(self.session))}')
        self._login()

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


class GetUserInfo:
    def __init__(self, session: requests.Session):
        self.session = session

    def getInfo(self):
        try:
            html = self.session.get(settings.USER_INFO_URL)
            soup = BeautifulSoup(html.text, 'html.parser')
            user_email = soup.find("div", {'style': 'width: 200px; float: left; overflow: hidden;'}).get_text().replace(
                u'\xa0', u'')
            user_name = soup.select_one("#user").text
            user_code = (soup.find("tr", {'style': 'height: 40px; vertical-align: middle;'}).
                         find_all("td")[1].text)[(soup.find("tr", {'style': 'height: 40px; vertical-align: middle;'}).
                                                  find_all("td")[1].text).find('(') + 1:(soup.find("tr", {'style': 'height: 40px; vertical-align: middle;'}).
                                                                                         find_all("td")[1].text).find(')')]  # 학번

            return user_name, user_code, user_email

        except Exception as e:
            log('error', 'session.GetUserInfo.getInfo',f'Exception {e}')
            return None
