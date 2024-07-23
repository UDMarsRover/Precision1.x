import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import time
import threading

class VideoStreamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'http Video Stream'
        self.left, self.top, self.width, self.height = 100, 100, 640, 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create a label to display the video stream
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width, self.height)

        # Set up the video capture
        # self.cap = cv2.VideoCapture('http://192.168.8.121:5000')  # Replace with your actual video stream URL
        self.cap = cv2.VideoCapture(0) # Replace with your actual video stream URL
        # Create a timer to update the video frame
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(30)  # Update every 30 milliseconds

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoStreamApp()
    keep_streaming = True
    def start_camera_thread():
        camera_thread = threading.Thread(target=update_stream)
        camera_thread.start()
    def stop_camera_thread():
        ex.cap.release()

    app.aboutToQuit.connect(stop_camera_thread)

    def update_stream():
        while keep_streaming:
            # print()
            ex.update_frame()
            time.sleep(0.03)

    start_camera_thread()
    print("SHOWING")
    ex.show()
    sys.exit(app.exec_())
