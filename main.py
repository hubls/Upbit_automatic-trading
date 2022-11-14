import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from overview import *
from PyQt5 import uic
from PyQt5.QtCore import *
from pyupbit import Upbit
#from volatility import *



class worker(QThread):
    def __init__(self, b):
        super().__init__()
        self.b = b

    def end(self):
        self.alive = False

    def run(self):
        hold_flag = False
        self.alive = True
        #target_price = get_target_price()

        while self.alive:
            now = datetime.datetime.now()
            mid = datetime.datetime(now.year, now.month, now.day)
            delta = datetime.timedelta(seconds=10)





class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)


        with open("upbit.txt", "r") as f:
            key0 = f.readline().strip()
            key1 = f.readline().strip()

        self.key0.setText(key0)
        self.key1.setText(key1)

        self.btn.setText("login")
        self.btn.clicked.connect(self.login)



    #이부분 수정 필요함
    def login(self):
        if self.btn.text() == "login":
            b = Upbit(self.key0.text(), self.key1.text())
            balance = b.get_balance("KRW")
            self.log.append(f"[로그인] 성공 / 현금 : {balance}")
            self.btn.setText("logout")

            #self.w = Worker(b)
            #self.w.start()

        else:
            # 자동매매 로직 종료
            #self.w.end()
            self.btn.setText("login")
            self.log.append(f"[로그아웃] 성공 / 자동매매종료")





    def closeEvent(self, event):
        self.overviewWidget.closeEvent(event)
        self.chartWidget.closeEvent(event)
        self.orderbookWidget.closeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    m  = MyWindow()
    m.show()
    app.exec_()