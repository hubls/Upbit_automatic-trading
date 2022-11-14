from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pyupbit
import time

class OrderbookWorker(QThread):
    dataReceive = pyqtSignal(list)

    def run(self):
        self.alive = True
        while self.alive:
            try:
                data = pyupbit.get_orderbook("KRW-BTC")
                self.dataReceive.emit(data)
            except:
                pass

            time.sleep(0.3)

    def end(self):
        self.alive = False

class OrderbookWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("orderbook.ui", self)

        self.asksAnim = []
        self.bidsAnim = []

        for i in range(10):
            d = QTableWidgetItem(str(""))
            d.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.askTable.setItem(i, 0, d)
            d = QTableWidgetItem(str(""))
            d.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.askTable.setItem(i, 1, d)
            d = QProgressBar(self.askTable)
            d.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            d.setStyleSheet("""
                QProgressBar        {background-color: rgba(0, 0, 0, 0) }
                QProgressBar::Chunk { background-color: rgba(255, 0, 0, 0.5) }
            """)
            anim = QPropertyAnimation(d, b"value")
            anim.setDuration(200)
            anim.setStartValue(0)
            self.asksAnim.append(anim)
            self.askTable.setCellWidget(i, 2, d)

            d = QTableWidgetItem(str(""))
            d.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.bidTable.setItem(i, 0, d)
            d = QTableWidgetItem(str(""))
            d.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.bidTable.setItem(i, 1, d)
            d = QProgressBar(self.bidTable)
            d.setStyleSheet("""
                QProgressBar        {background-color: rgba(0, 0, 0, 0) }
                QProgressBar::Chunk { background-color: rgba(0, 255, 0, 0.4) }
            """)
            d.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.bidTable.setCellWidget(i, 2, d)
            anim = QPropertyAnimation(d, b"value")
            anim.setDuration(200)
            anim.setStartValue(0)
            self.bidsAnim.append(anim)

        self.ow = OrderbookWorker()
        self.ow.dataReceive.connect(self.updataOrderbook)
        self.ow.start()

    def closeEvent(self, event):
        self.ow.end()

    def updataOrderbook(self, param):
        valueList = [ ]

        for idx in range(10):
            # 매도 호가
            item = param[0]['orderbook_units'][9 - idx]
            value = item['ask_price'] * item['ask_size']
            valueList.append(value)

            # 매수 호가
            item = param[0]['orderbook_units'][idx]
            value = item['bid_price'] * item['bid_size']
            valueList.append(value)

        maxTradingValue = max(valueList)

        for i in range(10):
            item = param[0]['orderbook_units'][9 - i]
            value = item['ask_price'] * item['ask_size']

            d = self.askTable.item(i, 0)
            d.setText(str(item['ask_price']))
            d = self.askTable.item(i, 1)
            d.setText(str(item['ask_size']))
            d = self.askTable.cellWidget(i, 2)
            d.setRange(0, int(maxTradingValue))
            d.setFormat(f"{value}")
            self.asksAnim[i].setStartValue(d.value())
            self.asksAnim[i].setEndValue(int(value))
            self.asksAnim[i].start()

            item = param[0]['orderbook_units'][i]
            value = item['bid_price'] * item['bid_size']
            d = self.bidTable.item(i, 0)
            d.setText(str(item['bid_price']))
            d = self.bidTable.item(i, 1)
            d.setText(str(item['bid_size']))
            d = self.bidTable.cellWidget(i, 2)
            d.setRange(0, int(maxTradingValue))
            d.setFormat(f"{value}")
            self.bidsAnim[i].setStartValue(d.value())
            self.bidsAnim[i].setEndValue(int(value))
            self.bidsAnim[i].start()



if __name__ == "__main__":
    app = QApplication([])
    ow  = OrderbookWidget()
    ow.show()
    app.exec_()