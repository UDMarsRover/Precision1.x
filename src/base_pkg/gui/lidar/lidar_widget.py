# lidar_widget.py
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QImage
import numpy as np
import math
import threading
import rospy
from sensor_msgs.msg import LaserScan 
import random


class LidarWidget(QtWidgets.QWidget):
    def __init__(self, dist):
        """
        Initializes the 
        """
        super().__init__()
        self.radius = dist# in m, the tangential distance to the edges of the square.
        # Set the pixel dimensions of the widget
        self.area_width = 700
        self.area_height = self.area_width
        self.setMinimumSize(self.area_width, self.area_height)
        self.setWindowTitle("Lidar Window")
        self.canvas = QtGui.QPixmap(self.area_width, self.area_height)
        self.canvas.fill(QtGui.QColor("black"))
        rover_real_height = 2
        rover_pixel_height = int((rover_real_height / (2 * self.radius)) * self.area_height)
        self.rover_image = QImage("src/base_pkg/gui/lidar/rover.png").scaledToHeight(rover_pixel_height, mode=Qt.FastTransformation)
        self.rover_image_x = self.area_height / 2 - self.rover_image.width() / 2
        self.rover_image_y = self.area_height / 2 - self.rover_image.height() / 2
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.draw_dots)
        self.timer.start(200)  # Update every 100ms
        self.dots = []
        self.painter = QPainter(self.canvas)
        self.num_points = 760
        self.x = np.zeros(self.num_points)
        self.y = np.zeros(self.num_points)
        self.setMouseTracking(True)
        self.pixel_label = QLabel(self)
        self.pixel_label.setStyleSheet("background-color: white; padding: 5px;")
        self.pixel_label.hide()  # Initially hidden

    def ros_callback(self, data):
        num_points = len(data.ranges)
        array = np.zeros((num_points, 2))
        for i in range(num_points):
            # Calculate angle of point
            array[i][0] = (i / float(num_points)) * 2 * math.pi
            # Get distance of point
            if not math.isinf(data.ranges[i]):
                array[i][1] = data.ranges[i]
            else:
                array[i][1] = 1000
        # Convert points to cartesian
        for i in range(num_points):
            array[i][0], array[i][1] = self.pol2cart(array[i][1], array[i][0])
        x = np.zeros(num_points)
        y = np.zeros(num_points)
        for i in range(num_points):
            x[i] = array[i][0]
            y[i] = array[i][1]
        point_scale = self.area_height / self.radius
        x = x * point_scale
        y = y * point_scale

        self.y, self.x = -x, -y

    def draw_dots(self):
        # Clear previous dots
        self.canvas.fill(QtGui.QColor("black"))

        # x, y = self.get_data()
        x, y = self.x, self.y
        for i in range(len(x)):
            x[i] = x[i] + self.area_width / 2
            y[i] = y[i] + self.area_height / 2
            self.dots.append((x[i], y[i]))
            # color = self.random_rainbow_color()
            # color = QtGui.QColor("red")
            color = self.calculate_gradient(self.distance(x[i], y[i]))
            self.painter.setBrush(QBrush(color, Qt.SolidPattern))
            self.painter.setPen(color)
            self.painter.drawEllipse(int(x[i]), int(y[i]), 1, 1)
        self.painter.drawImage(int(self.area_height / 2 - self.rover_image.width() / 2), int(self.area_height / 2 - self.rover_image.height() / 2), self.rover_image)
        self.update()

    def calculate_gradient(self, dist):
        dist = self.pixels_to_cm(dist)
        value_red = 0
        value_green = 0
        max_dist = self.radius - (self.pixels_to_cm(self.rover_image.width()) / 2)
        if dist < max_dist / 2:
            value_red = 255
            value_green = 255 * (dist / (max_dist / 2))
        else:
            value_green = 255
            value_red = 255 - (255 * (dist - (max_dist / 2) / (max_dist / 2)))

        if value_red > 255:
            value_red = 255
        if value_green > 255:
            value_green = 255
        if value_red < 0:
            value_red = 0
        if value_green < 0:
            value_green = 0
        
        return QColor(value_red, value_green, 0)

    def random_rainbow_color(self):
        # Define the rainbow colors (ROYGBIV)
        rainbow_colors = [
            QColor(255, 0, 0),   # Red
            QColor(255, 165, 0), # Orange
            QColor(255, 255, 0), # Yellow
            QColor(0, 255, 0),   # Green
            QColor(0, 0, 255),   # Blue
            QColor(75, 0, 130),  # Indigo
            QColor(148, 0, 211)  # Violet
        ]

        # Choose a random color from the rainbow
        return random.choice(rainbow_colors)

    def pol2cart(self, rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return(x, y)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.canvas)

    def pixels_to_cm(self, pixels):
        return pixels * ((self.radius * 2) / self.area_width)

    def mouseMoveEvent(self, event):
        # Get the cursor position in widget coordinates

        closest_distance = self.pixels_to_cm(self.distance(event.pos().x(), event.pos().y()))
        cursor_pos = event.pos()

        # Update the pixel label text
        self.pixel_label.setText(f"{closest_distance:.2f} m")

        # Set the position of the pixel label near the cursor
        label_offset = QPoint(10, -20)  # Adjust as needed
        self.pixel_label.move(cursor_pos + label_offset)

        # Show the pixel label
        self.pixel_label.show()
    
    def distance(self, x, y):
        # Calculate the x distance (dx) and y distance (dy)
        dx = max(self.rover_image_x - x,
                 0,
                 x - (self.rover_image_x + self.rover_image.width()))
        dy = max(self.rover_image_y - y,
                 0,
                 y - (self.rover_image_y + self.rover_image.height()))

        # Use the distance formula
        return (dx**2 + dy**2) ** 0.5
    
    class point():
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def x(self):
            return self.x
        def y(self):
            return self.y



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LidarWidget(3.0)
    window.show()
    sys.exit(app.exec_())
