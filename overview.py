import time
from pyupbit import WebSocketManager
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

class Worker(QThread):
    receiveData = pyqtSignal(dict)

    def run(self):
        wm = WebSocketManager("ticker", ["KRW-BTC"])
        self.alive = True

        while self.alive:
            try:
                data = wm.get()
                self.receiveData.emit(data)
                print(data)
            except:
                pass
            time.sleep(0.3)
        wm.terminate()

    def end(self):
        self.alive = False


class OverviewWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        uic.loadUi("overview.ui", self)

        self.w = Worker()
        self.w.receiveData.connect(self.processData)
        self.w.start()

    def closeEvent(self, event):
        self.w.end()

    def processData(self, data):
        self.price.setText(f"{data['trade_price']}")
        self.diff.setText(f"{data['signed_change_rate'] * 100:.2f} %")
        self.volume.setText(f"{data['acc_trade_volume_24h']}")
        self.value.setText(f"{data['acc_trade_price_24h'] / 100000000:,.2f}")
        self.high.setText(f"{data['high_price']}")
        self.low.setText(f"{data['low_price']}")
        self.prev.setText("-")
        self.updateStyle()


    def updateStyle(self):
        if self.diff.text()[0] == '-':
            self.price.setStyleSheet("color:blue")
            self.diff.setStyleSheet("color:white ; background-color:blue")
        else:
            self.price.setStyleSheet("color:red")
            self.diff.setStyleSheet("color:white ; background-color:red")

if __name__ == "__main__":
    app = QApplication([])
    m = OverviewWidget()
    m.show()
    app.exec_()
