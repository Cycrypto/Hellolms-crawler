import requests
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

    def getLectureList(self):
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
    def __init__(self, s: requests.Session):
        super().__init__(s)

    def getInformation(self, lecture_code, ref=settings.MAIN_URL):
        log('debug',SubjectInfo.getInformation.__name__, f"Go Classroom {lecture_code}")
        self.session.post(settings.AUTH_CHECK_URL, headers=settings.HEADER(ref))
        html = self.session.post(settings.INFORM_URL, data=settings.AUTH_FORM(UID, lecture_code))
        soup = BeautifulSoup(html.text, 'html.parser')
        table = soup.find('table')
        professor = table.select_one('#content_text > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(2)')\
            .text.strip()

        subject = return_form['subject'] = table.select_one('#content_text > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2)')\
            .text.strip()

        professor_email = 'None' if table.select_one('#content_text > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(4)').text.strip()[0] == '@' \
            else table.select_one('#content_text > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(4)').text.strip()

        book = table.select_one('#content_text > table:nth-child(3) > tbody > tr:nth-child(7) > td').text.strip()

        class_time = table.select_one('#content_text > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(2)').text.strip()

        print(professor, subject, professor_email, book, class_time)


if __name__ == "__main__":
    login = session.GetSession()
    lecture = SubjectInfo(login.session)
    lecture.getLectureList()
    lecture.getInformation(lecture.subject['데이터베이스(01)'])