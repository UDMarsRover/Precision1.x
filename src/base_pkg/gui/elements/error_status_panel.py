from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from errors_box import ErrorBox
import sys
import random

class ErrorStatusPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.error_boxes = []

    def add_error(self):
        error_box = ErrorBox()
        self.error_boxes.append(error_box)
        self.layout.addWidget(error_box)
        return error_box

    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = ErrorStatusPanel()
    for i in range(5):
        error_box = widget.add_error()
        error_box.set_name(f"Error {i}")
        error_box.set_id(i)
        error_box.set_status(random.randint(0, 3))
        for i in range(20):
            error_box.new_error(f"This is an error message ({i})")

    widget.show()

    sys.exit(app.exec_())