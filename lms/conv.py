from lms import _LOG
from lms import _settings as settings
from lms.session import GetSession

import json
import requests
import pandas as pd
from bs4 import BeautifulSoup


class Notifications:
    def __init__(self, s: requests.Session):
        self.session = s
        self.return_form = {
                'date': [],
                'content': [],
                'title': [],
            }

    def getList(self, start=1, display=5):
        inform_html = self.session.post(settings.NOTIFICATION_URL, data={'start': start, 'display': display})
        soup = BeautifulSoup(inform_html.text, 'html.parser')
        content = soup.find_all('div', {'class': 'notification_content'})   # 콘텐츠 접근

        for con in content:
            try:
                title = con.find('div', {'class': 'notification_subject'}).get_text().\
                    strip().replace("\r", '').replace("\n\n", '')

            except AttributeError:
                title = '-'

            try:        # 내용 받아오기
                body = con.find("div", {'class': 'notification_text'}).get_text().\
                    strip().replace("\r", '').replace("\n", '').replace("                                           ", ' ')

            except AttributeError:
                body = '-'

            try:        # 날짜 받아오기
                date = con.find("div", {'class': 'notification_day'}).get_text().\
                    strip().replace("\r", '').replace("\n\n", '')

            except AttributeError:
                date = '-'

            self.return_form['title'].append(title)
            self.return_form['content'].append(body)
            self.return_form['date'].append(date)

        return pd.DataFrame(self.return_form)

    def getUnreadCnt(self, start=1, display=5) -> str:
        html = self.session.post(settings.NOTIFICATION_COUNT_URL,  data={'start': start, 'display': display})
        data = html.json()
        return data['records'][0]['CNT']


if __name__ == "__main__":
    session = GetSession()
    login = session.session
    notification = Notifications(login)
    print(notification.getList())
    print(notification.getUnreadCnt())