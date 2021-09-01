import requests
import pandas as pd
import re
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
        url = settings.MAIN_URL  # 메인화면에 나와있는 과목명을 파싱할 예정
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
            raw_data = \
                str(k).strip().replace('(', '').replace(')', '').replace('\n', '').replace(' ', '').split('</em>')[0]
            start, end = raw_data.find("kj="), raw_data.find("kj_auth=")
            key.append(raw_data[start + 4: end - 1])

        ### MATCH SUBJECT AND KEY ###
        for idx, k in enumerate(self.subject.keys()):
            self.subject[k] = key[idx]
        log('info', Lecture.getLectureList.__name__, 'Get Subject Info Successfully!')


class SubjectInfo(Lecture):
    def __init__(self, s: requests.Session, class_name, ref) -> None:
        super().__init__(s)
        if any(self.subject) is False:  # 만약 subject 가 크롤링되지 않았다면 크롤링 실행
            self.getLectureList()

        self.subject_key = self.subject[class_name]
        log('debug', SubjectInfo.__name__, f"Go Classroom {class_name}")
        self.session.post(settings.AUTH_CHECK_URL, headers=settings.HEADER(ref),
                          data=settings.AUTH_FORM(self.subject_key))

    def getAnnounce(self) -> pd.DataFrame:
        """
        강의 공지에 대한 메서드입니다.
        :return:
        """
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

    def getClassInfo(self) -> pd.DataFrame:
        """
        강의 계획서를 로드하는 메서드입니다.
        :return:
        """
        return_form = {'form': {
            'subject': '',
            'subject_code': '',
            'professor': '',
            'category': '',
            'credit': '',
            'email': '',
            'book': '',
            'time': '',
            'eval_method': ''
        }
        }
        html = self.session.get(settings.PLANNER_URL)
        soup = BeautifulSoup(html.text, 'html.parser')
        table = soup.find('table')
        return_form['form']['professor'] = table.select_one(
            '#content_text > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(2)').text.strip()

        return_form['form']['subject'] = table.select_one(
            '#content_text > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2)').text.strip()

        return_form['form']['subject_code'] = table.select_one(
            '#content_text > table:nth-child(3) > tbody > tr:nth-child(2) > td:nth-child(2)').text.strip()

        return_form['form']['category'] = table.select_one(
            '#content_text > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(2)').text.strip()

        return_form['form']['credit'] = table.select_one(
            '#content_text > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(4)').text.strip()

        return_form['form']['email'] = 'None' if table.select_one(
            '#content_text > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(4)').text.strip()[0] == '@' \
            else table.select_one('#content_text > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(4)'). \
            text.strip()

        return_form['form']['book'] = table.select_one(
            '#content_text > table:nth-child(3) > tbody > tr:nth-child(7) > td').text.strip()

        return_form['form']['time'] = table.select_one(
            '#content_text > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(2)').text.strip()

        return_form['form']['eval_method'] = table.select_one(
            '#content_text > table:nth-child(3) > tbody > tr:nth-child(8) > td').text.strip()

        return pd.DataFrame(return_form)

    def getLectureMeterial(self) -> pd.DataFrame:
        """
        강의 자료에 관한 메서드입니다
        :return:
        """
        return_form = {
            'title': [],
            'seq_code': [],
            'seq_url': [],
            'upload_date': [],
        }
        html = self.session.get(settings.METERIAL_URL)
        soup = BeautifulSoup(html.text, 'html.parser')
        table = soup.find("table").find("tbody").find_all("tr")
        for t in table:
            return_form['title'].append(t.find_all("td")[2].find_all("div")[0].get_text().strip())
            return_form['upload_date'].append(t.find_all("td")[4].get_text().strip())

            return_form['seq_code'].append(
                re.findall(r'\(([^)]+)', t.find_all("td")[3].find("img")['onclick'])[0][1:-1] if t.find_all("td")[3].find("img") is not None else '')
            # 파일 다운로드를 위한 seq code
        for content in return_form['seq_code']:
            if content == '':
                return_form['seq_url'].append('None')

            else:
                inform_html = self.session.post('http://eclass.kpu.ac.kr/ilos/co/list_file_list2.acl',
                                                data=settings.FILE_DOWNLOAD_FORM(UID, self.subject_key, content))
                soup = BeautifulSoup(inform_html.text, 'html.parser')
                urlList = soup.find_all("div", {'class': 'list_div'})

                for ulist in urlList:
                    # ulist.find('a').find("href'")
                    download_url = 'http://eclass.kpu.ac.kr' + str(ulist.find('a'))[
                                                               str(ulist.find('a')).find("href") + 6: str(
                                                                   ulist.find('a')).find("pf_st_flag") - 1]
                    if download_url.split('/')[4] == 'co':  # 압축파일이 아닌경우
                        download_url = download_url.replace(';', '&')  # 파일 다운로드 링크 생성

                    return_form['seq_url'].append(download_url)

        return pd.DataFrame(return_form)

    def getHomework(self) -> pd.DataFrame:
        return_form = {
            'title': [],  # 제목
            'progress': [],  # 진행 여부
            'issubmit': [],  # 제출여부
            'score': [],  # 점수
            'distribution': [],  # 배점
            'deadline': [],
            'rt_seq': []  # 과목방 들어갈떄 씀
        }
        html = self.session.get(settings.HOMEWORK_URL)
        soup = BeautifulSoup(html.text, 'html.parser')
        table = soup.find("table").find("tbody").find_all("tr")
        for t in table:
            return_form['title'].append(t.find_all("td")[2].find_all("div")[0].get_text().strip())
            return_form['progress'].append(t.find_all("td")[3].get_text().strip())
            return_form['issubmit'].append(
                '제출' if len(t.find_all("td")[4].find_all("img", {'alt': '제출'})) != 0 else '미제출')
            return_form['score'].append(t.find_all("td")[5].get_text().strip())
            return_form['distribution'].append(t.find_all("td")[6].get_text().strip())
            return_form['deadline'].append(t.find_all("td")[7].get_text().strip())
            return_form['rt_seq'].append(str(re.findall(r'\(([^)]+)', str(t.find_all("td")[2].attrs['onclick']))[0][45:52]))

        return pd.DataFrame(return_form)


if __name__ == "__main__":
    login = session.GetSession()

    lecture = SubjectInfo(login.session, '파이썬프로그래밍(01)', settings.CURRENT)
    lecture.getLectureList()
    print(lecture.getHomework())
