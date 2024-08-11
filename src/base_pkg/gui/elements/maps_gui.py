import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QPixmap, QImage, QPainter, QFont, QPen
from PyQt5.QtCore import Qt
TL_COORD = (51.472573, -112.758359)
BR_COORD = (51.468584, -112.748124)


class ImageWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.breadcrumbs = []
        self.coord = (0, 0)
        self.image_path = image_path
        self.scale_factor = 1.0
        self.gps_width = TL_COORD[1] - BR_COORD[1]
        self.gps_height = TL_COORD[0] - BR_COORD[0]
        self.init_ui()
        # self.add_gps_point(51.471, -112.753)
        

    def init_ui(self):
        layout = QVBoxLayout(self)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        image_label = QLabel()
        self.image = QImage(self.image_path)
        image_label.setPixmap(QPixmap.fromImage(self.image))
        
        scroll_area.setWidget(image_label)
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        self.set_coord(51.4710000, -112.7530000)

    def wheelEvent(self, event):
        event.ignore()
        delta = event.angleDelta().y()
        if delta > 0:
            self.scale_factor *= 1.1
        else:
            self.scale_factor *= 0.9

        self.scale_factor = max(0.1, self.scale_factor)
        self.scale_factor = min(10, self.scale_factor)

        self.scale_image()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.last_pos
        self.last_pos = event.pos()
        scroll_area = self.findChild(QScrollArea)
        scroll_area.horizontalScrollBar().setValue(scroll_area.horizontalScrollBar().value() - delta.x())
        scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().value() - delta.y())

    def scale_image(self):
        image_label = self.findChild(QLabel)
        image = QImage(self.image_path)
        scaled_image = self.image.scaled(int(self.image.width() * self.scale_factor), int(self.image.height() * self.scale_factor), Qt.KeepAspectRatio)
        image_label.setPixmap(QPixmap.fromImage(scaled_image))


    def plot_breadcrumbs(self):
        painter = QPainter(self.image)
        pen = QPen(Qt.red)
        pen.setWidth(5)
        painter.setPen(pen)

        for point in self.breadcrumbs:
            x = (point[1] - BR_COORD[1]) / self.gps_width * self.image.width()
            y = (point[0] - BR_COORD[0]) / self.gps_height * self.image.height()
            painter.drawEllipse(int(x - 2.5), int(y - 2.5), 5, 5)
        painter.end()

    def add_breadcrumb(self, lat, lon):
        self.breadcrumbs.append((lat, lon))
        self.plot_breadcrumbs()
        self.update()

    def set_coord(self, lat, lon):
        self.coord = (lat, lon)
        painter = QPainter(self.image)
        pen = QPen(Qt.green)
        pen.setWidth(5)
        painter.setPen(pen)
        x = (lon - BR_COORD[1]) / self.gps_width * self.image.width()
        y = (lat - BR_COORD[0]) / self.gps_height * self.image.height()
        painter.drawEllipse(int(x - 10), int(y - 10), 20, 20)
        painter.end()
        self.add_breadcrumb(lat, lon)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_widget = ImageWidget('/home/ryan/Projects/Precision1.x/src/base_pkg/gui/elements/traversal_map.png')
    
    image_widget.show()
    sys.exit(app.exec_())