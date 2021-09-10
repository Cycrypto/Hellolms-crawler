from lms import _LOG
from lms import _settings as settings
from lms.session import GetSession

import json
import requests
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
        print(len(content))
        for con in content:
            title = con.find('div', {'class': 'notification_subject'}).get_text().strip().replace("\r", '').replace(
                "\n\n", '')
            body = con.find("div", {'class': 'notification_text'}).get_text().strip().replace("\r", '').replace(
                "\n", '') \
                .replace("                                           ", ' ')
            date = con.find("div", {'class': 'notification_day'}).get_text().strip().replace("\r", '').replace(
                "\n\n", '')
            print(title, body, date)
            self.return_form['title'].append(title)
            self.return_form['content'].append(body)
            self.return_form['title'].append(date)

            return self.return_form

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