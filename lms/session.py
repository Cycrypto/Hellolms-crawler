import os
import requests
import json
import pprint
import lms
from bs4 import BeautifulSoup
from lms import _LOG as log
import lms._settings as settings

import lms_db.query as db
lms._DEBUG = True      # 디버그모드 비활성화


def check_id_exist(path=settings.OWN_LOGIN_INFO_DB):
    q = db.Query(path)
    query = """SELECT * FROM USER_INFO"""
    q._cursor.execute(query)
    length = len(q._cursor.fetchall())
    del q
    if length == 1:
        return True

    else:
        return False


def get_id(path=settings.OWN_LOGIN_INFO_DB):
    global uid, pw
    q = db.Query(db=path)
    if check_id_exist(path) is True:
        query = """SELECT ID FROM USER_INFO"""
        q._cursor.execute(query)
        uid = q._cursor.fetchone()[0]

        query = """SELECT PW FROM USER_INFO"""
        q._cursor.execute(query)
        pw = q._cursor.fetchone()[0]
    else:
        uid = pw = None
    del q
    return uid, pw


class GetSession:
    def __init__(self):
        print("a")
        self.session = requests.Session()
        log('debug', 'session.GetSession.__init__', f'SESSION ID : {str(id(self.session))}')
        self._login()

    def _login(self) -> bool:
        uid, pwd = get_id()
        if settings.USER_INFO['usr_id'] is None:     # FOR DEBUG
            settings.USER_INFO['usr_id'] = uid

        if settings.USER_INFO['usr_pwd'] is None:
            settings.USER_INFO['usr_pwd'] = pwd

        log('info', 'session.GetSession.__init__', 'login start')
        self.session.post(settings.LOGIN_URL, data=settings.USER_INFO)

        if GetUserInfo(self.session).getInfo() is not None:
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


if __name__ == "__main__":
    login = GetSession()
    # print(GetUserInfo(login).getInfo())
