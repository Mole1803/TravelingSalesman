from copy import copy

from PySide6.QtCore import QObject
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QListView, QTableView, QTableWidget


def run():
    """Runs the UI"""
    app = QtWidgets.QApplication([])
    window = MainApplication()
    window.show()
    app.exec()


class CCanvas(QtWidgets.QGraphicsView):
    click_signal = QtCore.Signal(int, int)

    def __init__(self, parent=None, size=(600, 400), offset=(25, 25), background_color=(255, 255, 255), point_radius=6):
        super().__init__(parent)
        # Setup
        # self.controller = CCanvasController(self)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setGeometry(offset[0], offset[1], size[0], size[1])
        # Sizing
        self.setMinimumSize(size[0], size[1])
        self.setMaximumSize(size[0], size[1])
        self.setSceneRect(0, 0, size[0], size[1])
        self.ViewportAnchor = QtWidgets.QGraphicsView.ViewportAnchor.NoAnchor
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.background_color = background_color
        # Coloring
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(*self.background_color), QtCore.Qt.BrushStyle.SolidPattern))
        self.point_radius = point_radius

        # Misc
        self.setMouseTracking(True)
        # self.scene.addLine(0, 0, 100, 100, pen=QtGui.QPen(self.color, self.pen_size))

    def mousePressEvent(self, event):
        points = self.mapToScene(event.pos())
        pos_x = points.x()
        pos_y = points.y()
        self.click_signal.emit(pos_x, pos_y)

    def draw_point(self, x, y, point_color=(0, 0, 0)):
        self.scene.addEllipse(x, y, self.point_radius, self.point_radius,
                              pen=QtGui.QPen(QtGui.QColor(*point_color), self.point_radius))

    def draw_path(self, x_1,y_1,x_2,y_2, path_color=(0, 255, 0)):
        thickness = 2
        self.scene.addLine(x_1, y_1, x_2, y_2, pen=QtGui.QPen(QtGui.QColor(*path_color), thickness))

    def clear(self):
        self.scene.clear()
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(*self.background_color), QtCore.Qt.BrushStyle.SolidPattern))



class CTableWidget(QtCore.QAbstractTableModel):
    def __init__(self, data, headers=None, parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = headers

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        #center text
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, parent=None):
        """Set number of rows"""
        return len(self._data)

    def columnCount(self, parent=None):
        """Set number of columns"""
        return len(self._data[0])

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        """Set headers for table"""
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return self._headers[section]







class CTableView(QTableView):
    def __init__(self, parent=None, size=(250, 550), offset=(650, 25)):
        super().__init__(parent)

        self.setMinimumSize(size[0], size[1])
        self.setMaximumSize(size[0], size[1])
        self.setGeometry(offset[0], offset[1], size[0], size[1])
        self.model = None
        # disable vertical header
        self.verticalHeader().setVisible(False)
        # horizontal header
        self.horizontalScrollBar().setDisabled(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #f0f0f0; border: 1px solid #6c6c6c;color: #000000; font-weight: bold;}")

    def set_model(self, data, headers):
        self.model = CTableWidget(data, headers)
        self.setModel(self.model)



class MainApplication(QtWidgets.QWidget):
    """Main view for the application"""


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(900, 600)
        self.setWindowTitle("Main Application")

        self.canvas = CCanvas(self)

        self.list_view = CTableView(self)
        self.start_button = QtWidgets.QPushButton("Start", self)
        self.clear_button = QtWidgets.QPushButton("Clear", self)
        self.start_button.setGeometry(650, 600, 100, 30)

        self.clear_button.setGeometry(750, 600, 100, 30)



