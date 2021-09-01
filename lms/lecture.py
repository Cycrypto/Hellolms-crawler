import requests
import pandas as pd
import lms._settings as settings

import lms.session as session
from bs4 import BeautifulSoup
from lms import _LOG as log
from __own.Account import UID


class Lecture:
    def __init__(self, s: requests.Session):
        self.session = s
        self.subject = {}
        log('debug', Lecture.__name__, f'SESSION ID : {id(self.session)}')

    def getLectureList(self) -> None:
        url = settings.MAIN_URL     # 메인화면에 나와있는 과목명을 파싱할 예정
        req = self.session.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        key = []
        sub_screen = soup.find_all("em", {'class': 'sub_open'})

        ### GET SUBJECT NAME ###
        for sj_num in sub_screen:
            subjt = sj_num.get_text().strip().replace(' ', '').replace('\r\n\r\n', '')
            self.subject[subjt] = None

        ### GET SUBJECT KEY ###
        for k in soup.find_all('em', {'class': 'sub_open'}):
            raw_data = str(k).strip().replace('(', '').replace(')', '').replace('\n', '').replace(' ', '').split('</em>')[0]
            start, end = raw_data.find("kj="), raw_data.find("kj_auth=")
            key.append(raw_data[start+4: end-1])

        ### MATCH SUBJECT AND KEY ###
        for idx, k in enumerate(self.subject.keys()):
            self.subject[k] = key[idx]
        log('info', Lecture.getLectureList.__name__, 'Get Subject Info Successfully!')


class SubjectInfo(Lecture):
    def __init__(self, s: requests.Session, class_name, ref):
        super().__init__(s)

        if any(self.subject) is False:  # 만약 subject 가 크롤링되지 않았다면 크롤링 실행
            self.getLectureList()

        log('debug', SubjectInfo.getInformation.__name__, f"Go Classroom {class_name}")
        self.session.post(settings.AUTH_CHECK_URL, headers=settings.HEADER(ref),
                          data=settings.AUTH_FORM(self.subject[class_name]))

    def getInformation(self):
        data = {
            'inform': [],
            'title': [],
            'file': [],
            'date': []
        }

        html = self.session.get(settings.INFORM_URL)
        soup = BeautifulSoup(html.text, 'html.parser')
        body = soup.find('table').find('tbody').find_all('tr')

        for tb in body:
            data['inform'].append('-' if tb.find_all("td")[0].find("img") is None else "중요")
            data['title'].append(tb.find_all("td")[2].find_all("div")[0].get_text())
            data['file'].append('첨부파일 없음' if tb.find_all("td")[3].get_text() != '' else '첨부파일 있음')
            data['date'].append((tb.find_all("td")[4].get_text()))

        return pd.DataFrame(data)


if __name__ == "__main__":
    login = session.GetSession()

    lecture = SubjectInfo(login.session, '데이터베이스(01)', settings.CURRENT)
    lecture.getLectureList()
    print(lecture.getInformation())