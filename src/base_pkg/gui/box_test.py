import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
       
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('Utilizing PyQt Box Layouts: QHBoxLayout and QVBoxLayout')  
        self.show()

if __name__ == '__main__':
 app = QApplication(sys.argv)
 ex = Example()
 sys.exit(app.exec_())