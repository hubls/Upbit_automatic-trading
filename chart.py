from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtChart import *
from PyQt5.QtGui import *
import pybithumb
import time
import pyupbit

#빗썸으로 구현되어있어서 수정해야됨

class ChartWorker(QThread):
    dataSent = pyqtSignal(int)
    def run(self):
        self.alive = True
        while self.alive:
            try:
                price = pyupbit.get_current_price("KRW-BTC")
                self.dataSent.emit(price)
            except:
                pass

            time.sleep(1)

    def end(self):
        self.alive = False

class ChartWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        uic.loadUi("chart.ui", self)

        #1) 데이터 추가
        self.priceData = QLineSeries()

        #df = pybithumb.get_ohlcv("BTC")



        #2) 도화지 연결
        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)
        self.priceChart.legend().hide()
        self.priceChart.layout().setContentsMargins(0, 0, 0, 0)

        ax = QDateTimeAxis()
        ax.setFormat("hh:mm:ss")
        ax.setTickCount(4)
        self.priceChart.addAxis(ax, Qt.AlignBottom)

        ay = QValueAxis()
        self.priceChart.addAxis(ay, Qt.AlignLeft)


        self.priceData.attachAxis(ax)
        self.priceData.attachAxis(ay)


        #3) 위젯에 출력

        self.priceView.setChart(self.priceChart)
        self.priceView.setRenderHints(QPainter.Antialiasing)

        self.cw = ChartWorker()
        self.cw.dataSent.connect(self.appendData)
        self.cw.start()


        self.viewLimit = 60

    def closeEvent(self, event):
        self.cw.end()

    def appendData(self, price):

        if len(self.priceData) == self.viewLimit:
            self.priceData.remove(0)

        curr = QDateTime.currentDateTime()
        self.priceData.append(curr.toMSecsSinceEpoch(), price)

        pvs = self.priceData.pointsVector()
        x = int(pvs[0].x())

        s = QDateTime.fromMSecsSinceEpoch(x)
        e = s.addSecs(self.viewLimit)

        ax = self.priceChart.axisX()
        ax.setRange(s, e)

        ay = self.priceChart.axisY()
        dataY = [item.y() for item in pvs]

        minVal = min(dataY)
        maxVal = max(dataY)
        margin = (maxVal - minVal) * 0.2

        ay.setRange(minVal - margin, maxVal + margin)



if __name__ == "__main__":
    app = QApplication([])
    m = ChartWidget()
    m.show()
    app.exec_()