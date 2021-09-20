import sys
import lms
import requests
import lms.session as session
from lms import _LOG as log
from PyQt5.QtWidgets import *
from PyQt5 import uic

MAIN_DIR = r'../../resources/Agenda.ui'
MAIN_FORM = uic.loadUiType(MAIN_DIR)[0]
lms._DEBUG = True   # 디버그 모드 활성화


class MainWindow(QMainWindow, MAIN_FORM):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setLoginInfo()
        self.login: requests.Session = session.GetSession().session

    def setLoginInfo(self):
        try:
            name, number, email = session.GetUserInfo(self.login).getInfo()
            self.label.setText(f"{name}({number}) - {email}님 환영합니다")

        except Exception as e:
            log("info", "ui-event.setLoginInfo", f"{e}")
            self.label.setText(f"세션에 접속하는데 실패했습니다")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec()
