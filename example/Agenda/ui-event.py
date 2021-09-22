import sys
import lms
import requests
import lms._settings as settings
import lms.session as session
import lms.lecture as lecture
from lms import _LOG as log
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import uic

MAIN_DIR = r'../../resources/Agenda.ui'
MAIN_FORM = uic.loadUiType(MAIN_DIR)[0]
lms._DEBUG = True   # 디버그 모드 활성화


def autoResizeTable(table: QTableWidget):
    header = table.horizontalHeader()
    twidth = header.width()
    width = []
    for column in range(header.count()):
        header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
        width.append(header.sectionSize(column))
    wfactor = twidth / sum(width)
    for column in range(header.count()):
        header.setSectionResizeMode(column, QHeaderView.Interactive)
        header.resizeSection(column, int(width[column] * wfactor))


class MainWindow(QMainWindow, MAIN_FORM):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.login: requests.Session = session.GetSession().session
        self.setLoginInfo()
        self.user_subject = self.setSubjectList()   # 과목과, 과목코드를 크롤링해와서 저장
        self.subjectInfoTable(list(self.user_subject.subject.keys())[0])    # 기본값으로 0번째 데이터를 가져옴
        self.classInfoTable(list(self.user_subject.subject.keys())[0])    # 기본값으로 0번째 데이터를 가져옴
        self.reportInfoTable(list(self.user_subject.subject.keys())[0])    # 기본값으로 0번째 데이터를 가져옴

    def setLoginInfo(self):
        try:
            name, number, email = session.GetUserInfo(self.login).getInfo()
            self.label.setText(f"{name}({number}) - {email}님 환영합니다")

        except Exception as e:
            log("info", "ui-event.setLoginInfo", f"{e}")
            self.label.setText(f"세션에 접속하는데 실패했습니다")

    def setSubjectList(self) -> lecture.Lecture:
        user_class = lecture.Lecture(self.login)
        user_class.getLectureList()     # 과목 크롤링 후 업데이트
        subjects = user_class.subject
        for sub in subjects.keys():
            self.listWidget.addItem(sub)

        return user_class

    def subjectInfoTable(self, class_name):
        subject_info = lecture.SubjectInfo(self.login, class_name, settings.CURRENT)
        class_info: pd.DataFrame = subject_info.getClassInfo()
        dict_form: dict = class_info.to_dict()  # 딕셔너리로 이동
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(len(dict_form['form'].keys()))
        self.tableWidget.horizontalHeader().setDefaultSectionSize(360)
        self.tableWidget.setVerticalHeaderLabels(list(dict_form['form'].keys()))
        self.tableWidget.setHorizontalHeaderLabels(['과목 정보'])

        for i, key in enumerate(dict_form['form'].keys()):
            self.tableWidget.setItem(1, i - 1, QTableWidgetItem(dict_form['form'][key]))

    def classInfoTable(self, class_name):
        subject_info = lecture.SubjectInfo(self.login, class_name, settings.CURRENT)
        subject_announcement: pd.DataFrame = subject_info.getAnnounce()
        dict_form: dict = subject_announcement.to_dict()  # 딕셔너리로 이동

        self.tableWidget_2.setColumnCount(len(dict_form.keys()))
        self.tableWidget_2.setRowCount(len(dict_form['inform']))
        self.tableWidget_2.setHorizontalHeaderLabels(list(dict_form.keys()))
        # autoResizeTable(self.tableWidget_2)
        for i in range (len(dict_form['inform'])):
            for j in range (len(dict_form.keys())):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(dict_form[list(dict_form.keys())[j]][i]))

    def reportInfoTable(self, class_name):
        subject_info = lecture.SubjectInfo(self.login, class_name, settings.CURRENT)
        subject_announcement: pd.DataFrame = subject_info.getHomework()
        dict_form: dict = subject_announcement.to_dict()  # 딕셔너리로 이동
        print(dict_form)
        self.tableWidget_3.setColumnCount(len(dict_form.keys()))
        self.tableWidget_3.setRowCount(len(dict_form['title']))
        self.tableWidget_3.setHorizontalHeaderLabels(list(dict_form.keys()))
        # autoResizeTable(self.tableWidget_2)
        for i in range(len(dict_form['title'])):
            for j in range(len(dict_form.keys())):
                self.tableWidget_3.setItem(i, j, QTableWidgetItem(dict_form[list(dict_form.keys())[j]][i]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec()
