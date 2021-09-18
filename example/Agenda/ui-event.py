import sys
import lms
from lms import session
from PyQt5.QtWidgets import *
from PyQt5 import uic

MAIN_DIR = r'../../resources/Agenda.ui'
MAIN_FORM = uic.loadUiType(MAIN_DIR)[0]
lms._DEBUG = True   # 디버그 모드 활성화


class MainWindow(QMainWindow, MAIN_FORM):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    app.exec()