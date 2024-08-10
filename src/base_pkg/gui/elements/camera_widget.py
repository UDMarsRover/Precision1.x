import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import time
import threading

class CameraWidget(QWidget):
    def __init__(self, camera_url="http://192.168.8.223:8080", width=640, height=480):
        super().__init__()
        self.title = 'http Video Stream'
        self.left, self.top, self.width, self.height = 0, 0, width, height
        self.camera_url = camera_url
        self.setStyleSheet("background-color: black;")
        self.initUI()
        self.run()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMaximumSize(self.width, self.height)

        # Create a label to display the video stream
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width, self.height)
        self.label.setContentsMargins(0, 0, 0, 0)

        # Set up the video capture
        # self.cap = cv2.VideoCapture('http://192.168.8.121:5000')  # Replace with your actual video stream URL
        self.cap = cv2.VideoCapture(self.camera_url) # Replace with your actual video stream URL

    def set_camera_url(self, camera_url):
        self.stop_camera_thread()
        self.camera_url = camera_url
        self.cap = cv2.VideoCapture(self.camera_url)
        self.start_camera_thread()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # rgb_image = frame
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap)

    def run(self):
        self.start_camera_thread()
    def start_camera_thread(self):
        self.camera_thread = threading.Thread(target=self.update_stream)
        self.keep_streaming = True
        self.camera_thread.start()

    def closeEvent(self, event):
        self.stop_camera_thread()
        self.camera_thread.join()
        event.accept()

    def stop_camera_thread(self):
        
        self.keep_streaming = False
        self.camera_thread.join()
        self.cap.release()
        
    

    def update_stream(self):
        while self.keep_streaming:
            # print()
            self.update_frame()
            time.sleep(0.03)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraWidget()

    print("SHOWING")
    ex.show()
    sys.exit(app.exec_())
