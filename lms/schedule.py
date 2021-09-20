import lms._settings as settings
import lms.session as session
import requests
import re
import pandas as pd
from lms import _LOG as log

from bs4 import BeautifulSoup


class Calendar:
    def __init__(self, s: requests.Session):
        self.session = s
        self.selected_date = None
        self.selected_time = None

    @property           # getter get date
    def date(self) -> str:
        return self.selected_date

    @date.setter     # setter
    def date(self, date:str):
        d = ''.join(filter(str.isalnum, date))
        self.selected_date = d

    @property
    def time(self):     # getter get time
        return self.selected_time

    @time.setter
    def time(self, time):   # setter
        t = ''.join(filter(str.isalnum, time))
        self.selected_time = t

    def readCalendar(self) -> dict:
        return_form = {
            'title': [],
            'content': [],
            'seq': []
        }
        inform_html = self.session.post(settings.MAIN_SCHEDULE_URL, data={'viewDt': self.date})
        soup = BeautifulSoup(inform_html.text, 'html.parser')
        title = soup.find_all("div", {'style': 'overflow: hidden; float: left;max-width: 480px;'})
        content = soup.find_all("div", {'style': 'overflow: hidden; clear: both;'})
        seq = soup.find_all("div", {'class': 'schedule-show-control'})

        for t in title:
            return_form['title'].append(t.get_text().replace('\r\n', '').replace('          ', ' ').strip())

        for c in content:
            return_form['content'].append(c.get_text().strip())

        for s in seq:
            dt_seq = s.attrs['onclick']
            items = re.findall(r'\(([^)]+)', dt_seq)
            return_form['seq'].append(items[0].replace('\"', '').split(',')[1])

        return return_form

    def insertSchedule(self, title, content) -> None:
        header = {'SCH_TITLE': title,
                  'SCH_CONTENTS': content,
                  'SCH_START_DT': self.selected_date,
                  'SCH_START_TM': self.selected_time,
                  'SCH_DV_CD': 1}

        inform_html = self.session.post(settings.INSERT_SCHEDULE_URL, data=header)
        return_json = inform_html.json()
        if return_json['isError']:
            log('error', 'schedule.Calendar.insertSchedule', '정보를 업로드하는데 실패했습니다.')

        else:
            log('info', 'schedule.Calendar.insertSchedule', '정보를 성공적으로 업로드했습니다.')

    def deleteSchedule(self, idx) -> None:
        try:
            seq = self.readCalendar()['seq'][idx][1:5]

        except IndexError:
            log('error', 'schedule.Calendar.deleteSchedule', '정보를 삭제하는데 실패했습니다.')
            return

        return_json = self.session.post(settings.DELETE_SCHEDULE_URL, data={"SCH_SEQ": seq}).json()

        if return_json['isError']:
            log('error', 'schedule.Calendar.deleteSchedule', '정보를 삭제하는데 실패했습니다.')

        else:
            log('info', 'schedule.Calendar.deleteSchedule', '정보를 성공적으로 삭제했습니다.')
        # DB를 이용한다면 수정 예정


if __name__ == "__main__":
    calendar = Calendar(session.GetSession().session)
    calendar.date = '2021-09-09'
    calendar.time = '21:19'

    calendar.insertSchedule("test", "test content")
    # calendar.deleteSchedule(0)