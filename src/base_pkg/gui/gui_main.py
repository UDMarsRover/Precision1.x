import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout, 
    QLabel, 
    QStackedLayout
 )

from PyQt5.QtGui import QPalette, QColor

class P(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(600, 200))

        layout = QHBoxLayout()

        emoLabel = QLabel("Emo Error")
        emoLabel.setStyleSheet("background-color: red; color: white;")
        emoLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(emoLabel)

        driveLabel = QLabel("Drive Error")
        driveLabel.setStyleSheet("background-color: red; color: white;")
        driveLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(driveLabel)

        armLabel = QLabel("Arm Error")
        armLabel.setStyleSheet("background-color: red; color: white")
        armLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(armLabel)

        camLabel = QLabel("Camera Error")
        camLabel.setStyleSheet("background-color: red; color: white")
        camLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(camLabel)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = P()
    window.show()

    app.exec()