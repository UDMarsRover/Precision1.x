

from random import randint
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
import numpy as np
import math

class DotPainter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.area_width = 500
        self.area_height = 500
        self.setMinimumSize(500, 500)
        self.setWindowTitle("Random Red Dots")
        self.canvas = QtGui.QPixmap(self.area_width, self.area_height)
        self.canvas.fill(QtGui.QColor("black"))
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.draw_dots)
        self.timer.start(50)  # Update every 100ms
        self.dots = []
        self.painter = QPainter(self.canvas)
        self.num_points = 560
        self.x = np.zeros(self.num_points)
        self.y = np.zeros(self.num_points)

    def draw_dots(self):
        # Clear previous dots
        self.canvas.fill(QtGui.QColor("black"))

        x, y = self.get_data()
        for i in range(len(x)):
            x[i] = x[i] + self.area_width / 2
            y[i] = y[i] + self.area_height / 2
            self.dots.append((x[i], y[i]))
            self.painter.setBrush(QBrush(QtGui.QColor("red"), Qt.SolidPattern))
            self.painter.setPen(QtGui.QColor("red"))
            self.painter.drawEllipse(int(x[i]), int(y[i]), 1, 1)

        self.update()

    def get_data(self):
        num_points = 1000
        array = np.zeros((num_points, 2))
        for i in range(num_points):
            array[i][0] = (i / float(num_points)) * 2 * math.pi
            array[i][1] = randint(100, 150)
        for i in range(num_points):
            array[i][0], array[i][1] = self.pol2cart(array[i][1], array[i][0])
        x = np.zeros(num_points)
        y = np.zeros(num_points)
        for i in range(num_points):
            x[i] = array[i][0]
            y[i] = array[i][1]
        return(x, y)
    
    def pol2cart(self, rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return(x, y)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.canvas)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DotPainter()
    window.show()
    sys.exit(app.exec_())
