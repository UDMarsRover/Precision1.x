import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMessageBox, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPainter, QColor
import PyQt5.QtCore as QtCore
import time
import datetime
class ErrorBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 300, 200)  # Set the size and position of the widget
        self.setMinimumSize(300, 200)
        self.set_color("green")
        self.name_label = QLabel()
        self.name_label.setStyleSheet("color: black; font-size: 30px;")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.id = ""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.name_label)
        self.setCursor(QtCore.Qt.PointingHandCursor)  # Set the cursor to a pointing hand
        self.errors = []
        self.popup = QMessageBox()
        self.errors_widget = QWidget()
        self.errors_layout = QVBoxLayout(self.errors_widget)
        
        
        self.generate_error_popup()


    def mousePressEvent(self, event):
        self.open_popup()

    def generate_error_popup(self):
        self.popup_internal_widget = QWidget()
        self.popup_internal_widget.setLayout(QVBoxLayout())
        self.popup.layout().addWidget(self.popup_internal_widget)
        self.popup_internal_widget.layout().setAlignment(QtCore.Qt.AlignCenter)
        self.id_label = QLabel()
        self.popup_internal_widget.layout().addWidget(self.id_label)
        self.scroll_area = QScrollArea()
        # scroll_layout = QVBoxLayout(scroll_widget)
        self.errors_widget.layout().addStretch(1)
        self.scroll_area.setMinimumSize(1000, 1200)
        self.scroll_area.setWidget(self.errors_widget)
        
        self.popup_internal_widget.layout().addWidget(self.scroll_area)
        # self.errors_widget.setMinimumWidth(4000)
        self.scroll_area.setWidgetResizable(True)

        ok_button = self.popup.addButton(QMessageBox.Ok)
        ok_button.setStyleSheet("font-size: 20px;")
        self.popup_internal_widget.layout().addWidget(ok_button)

    def open_popup(self):

        self.popup.setWindowTitle(self.name_label.text())
        self.id_label.setText(f"ID: {self.id}")
        self.popup.exec_()
    def set_color(self, color):
        self.setStyleSheet(f"background-color: {color};")

    def set_status(self, status):
        self.status = status
        if self.status == 0:
            self.set_color("green")
        elif self.status == 1:
            self.set_color("yellow")
        elif self.status == 2:
            self.set_color("red")
        else:
            self.set_color("gray")
        self.update()

    def set_name(self, name):
        self.name_label.setText(name)

    def set_id(self, id):
        self.id = id

    def new_error(self, error):
        timed_error = [error, time.time()]
        self.errors.append(timed_error)
        error_widget = self.ErrorLabel(timed_error[0], timed_error[1])
        self.errors_widget.layout().insertWidget(0, error_widget)

    class ErrorLabel(QWidget):
        def __init__(self, error, timestamp):
            super().__init__()
            self.layout = QVBoxLayout()
            # self.layout.addStretch(1)
            self.time_label = QLabel()
            self.error_label = QLabel()
            self.error_label.setStyleSheet("padding-right: 2em;")
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.error_label.setWordWrap(False)
            self.set_time(timestamp)
            self.set_error(error)
            self.layout.addWidget(self.time_label)
            self.layout.addWidget(self.error_label)
            self.setLayout(self.layout)

        def set_time(self, timestamp):
            time = datetime.datetime.fromtimestamp(timestamp)
            hour = time.hour
            minute = str(time.minute).zfill(2)
            second = str(time.second).zfill(2)
            ms = time.microsecond
            time_label = f"{hour}:{minute}:{second}"
            self.time_label.setText(time_label)

        def set_error(self, error):
            self.error_label.setText(error)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = ErrorBox()
    widget.set_name("Some Component")
    widget.set_id("some_component_id")
    widget.new_error("This is a new error. The element associated with this error is having some issues.")
    widget.new_error("This is a new error. The element associated with this error is having some issues.")
    widget.new_error("This is a new error. The element associated with this error is having some issues.")

    widget.show()

    sys.exit(app.exec_())