from copy import copy

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QListView



def run():
    """Runs the UI"""
    app = QtWidgets.QApplication([])
    window = MainApplication()
    window.show()
    app.exec()

class canvas(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setMinimumSize(600, 400)
        self.setMaximumSize(600, 400)
        self.setSceneRect(0, 0, 600, 400)
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255), QtCore.Qt.BrushStyle.SolidPattern))
        self.ViewportAnchor = QtWidgets.QGraphicsView.ViewportAnchor.NoAnchor
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.color = QtCore.Qt.GlobalColor.green
        self.pen_size = 2
        self.setMouseTracking(True)
        # Black background



        #self.scene.addLine(0, 0, 100, 100, pen=QtGui.QPen(self.color, self.pen_size))

    def mousePressEvent(self, event):
        points = self.mapToScene(event.pos())
        pos_x = points.x()
        pos_y = points.y()
        self.draw_point(pos_x, pos_y)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        pass

    def draw_point(self, x, y):
        radius = 4
        #Filled Ellipse
        self.scene.addEllipse(x, y, radius, radius, pen=QtGui.QPen(self.color, radius))


class CListView(QListView):
    def __init__(self,parent=None):
        super().__init__(parent)


class MainApplication(QtWidgets.QWidget):
    """Main view for the application"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Main Application")
        self.canvas = canvas(self)
        self.canvas.setGeometry(0, 0, 800, 600)
