import typing

from PySide6.QtCore import QObject
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QListView, QTableView, QTableWidget
from PySide6.QtGui import QBrush, QColor, QPen
from view.properties import Settings, CColor, CColorTheme

view_settings = Settings()


class CCanvas(QtWidgets.QGraphicsView):
    click_signal = QtCore.Signal(int, int)
    background_color = None

    def __init__(self, parent=None, size=(600, 400), pos=(25, 25), point_radius=6, settings=view_settings):
        super().__init__(parent)

        # Setup scene
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        # Sizing
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setMinimumSize(size[0], size[1])
        self.setMaximumSize(size[0], size[1])
        self.setSceneRect(0, 0, size[0], size[1])
        self.ViewportAnchor = QtWidgets.QGraphicsView.ViewportAnchor.NoAnchor
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        # Coloring
        self.settings = settings
        self.update_settings()

        # Drawing config
        self.point_radius = point_radius
        self.path_thickness = 2

        # Misc
        # self.setMouseTracking(True)

        # Scrollbar policy
        self.horizontalScrollBar().setEnabled(False)
        self.verticalScrollBar().setEnabled(False)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() != QtCore.Qt.MouseButton.LeftButton:
            return
        points = self.mapToScene(event.pos())
        pos_x = int(points.x())
        pos_y = int(points.y())
        valid_x = 0 <= pos_x <= self.width()
        valid_y = 0 <= pos_y <= self.height()
        if not valid_x or not valid_y:
            return

        self.click_signal.emit(pos_x, pos_y)

    def draw_point(self, x: int, y: int, point_color:str=None) -> None:
        """Draws a point on the canvas
        Args:
            x (int): x coordinate of point
            y (int): y coordinate of point
            point_color (str, optional): Color of path in hex. Defaults to None.
        """
        if point_color is None:
            point_color = self.settings.color_theme.CANVAS_POINT_COLOR
        self.scene.addEllipse(x, y, self.point_radius, self.point_radius,
                              pen=QtGui.QPen(QtGui.QColor(point_color), self.point_radius))

    def draw_path(self, x_1: int, y_1: int, x_2: int, y_2: int, path_color:str= None) -> None:
        """Draws a path between two points on the canvas
        Args:
            x_1 (int): x coordinate of first point
            y_1 (int): y coordinate of first point
            x_2 (int): x coordinate of second point
            y_2 (int): y coordinate of second point
            path_color (str, optional): Color of path in hex. Defaults to None.
        """
        if path_color is None:
            path_color = self.settings.color_theme.CANVAS_PATH_COLOR
        self.scene.addLine(x_1, y_1, x_2, y_2, pen=QPen(QColor(path_color), self.path_thickness))

    def clear(self):
        self.scene.clear()
        self.init_background()

    def init_background(self):
        self.scene.setBackgroundBrush(QBrush(QColor(self.background_color)))

    def update_settings(self):
        self.update_theme()

    def update_theme(self):
        self.background_color = self.settings.color_theme.CANVAS_BACKGROUND_COLOR
        self.clear()


class CTableWidget(QtCore.QAbstractTableModel):
    def __init__(self, data, headers=None, parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = headers

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        # center text
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, parent=None):
        """Set number of rows"""
        if self._data is None and self._headers is None:
            return 0

        if len(self._data) > 0:
            return len(self._data)

        if len(self._headers) > 0:
            return 0

    def columnCount(self, parent=None):
        """Set number of columns"""
        if self._data is None and self._headers is None:
            return 0

        if len(self._headers) > 0:
            return len(self._headers)

        if len(self._data) > 0:
            return len(self._data[0])

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation,
                   role: int = QtCore.Qt.ItemDataRole.DisplayRole) -> typing.Any:
        """Set headers for table
        Args:
            section (int): column number
            orientation (QtCore.Qt.Orientation): horizontal or vertical
            role (int, optional): Defaults to QtCore.Qt.ItemDataRole.DisplayRole
        Returns:
            typing.Any: header data
        """
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return self._headers[section]


class CTableView(QTableView):
    def __init__(self, parent=None, size=(300, 550), pos=(0, 0)):
        super().__init__(parent)
        self.settings = parent.settings

        self.setMinimumSize(size[0], size[1])
        self.setMaximumSize(size[0], size[1])
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.model = None
        # disable vertical header
        self.verticalHeader().setVisible(False)
        # horizontal header
        self.horizontalScrollBar().setDisabled(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.update_settings()

    def set_model(self, data, headers):
        self.model = CTableWidget(data, headers)
        self.setModel(self.model)

    def update_settings(self):
        self.update_theme()

    def update_theme(self):
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section {"
            f"background-color: transparent;"
            f"color: {self.settings.color_theme.LIGHT_TEXT_COLOR};"
            f" font-weight: bold;"
            f"border: 5px solid transparent;"
            f"font-size: {self.settings.font_size_large}px;"
            "}"

        )

        self.setStyleSheet("QTableView {"
                           f"background-color: {self.settings.color_theme.BACKGROUND_COLOR};"
                           f" border: 3px solid {self.settings.color_theme.ACCENT_COLOR};"
                           "border-radius: 5px;"
                           "padding: 5px;"
                           "}"

                           "QTableView::item {"
                           f"background-color: {self.settings.color_theme.BACKGROUND_COLOR};"
                           f"font-size: {self.settings.font_size_medium}px;"
                           "}"
                           "QTableView::item: selected {"
                           f"background-color: {self.settings.color_theme.ACCENT_COLOR};"
                           "}"
                           )

        self.setShowGrid(False)
        self.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical {"
            "background-color: transparent;"
            "color: transparent;"
            "} "

            "QScrollBar::handle:vertical:hover {"
            f"border: 1px solid {self.settings.color_theme.ON_HOVER_COLOR};"
            "border-radius: 5px;"
            "}"

            "QScrollBar::handle:vertical {"
            f"border: 1px solid {self.settings.color_theme.SECONDARY_COLOR};"
            "border-radius: 5px;"
            "}"
        )


class CButton(QtWidgets.QPushButton):
    theme = None

    def __init__(self, parent=None, text="Button", size=(100, 30), pos=(0, 0), settings=view_settings):
        super().__init__(parent)
        self.setMinimumSize(size[0], size[1])
        self.setMaximumSize(size[0], size[1])
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setText(text)

        self.settings = settings
        self.update_settings()

    def update_settings(self):
        self.update_theme()

    def update_theme(self):
        self.theme = self.settings.color_theme
        self.setStyleSheet("QPushButton {"
                           f"background-color: {self.theme.ACCENT_COLOR};"
                           f" border: 0px solid transparent;"
                           f" color: {self.theme.ACCENT_TEXT_COLOR};"
                           f" font-weight: bold;"
                           f" border-radius: 5px;"
                           "}"
                           
                           "QPushButton:hover {"
                           f" border: 1px solid {self.theme.ON_HOVER_COLOR};"
                           "}")


class CFrame(QtWidgets.QFrame):
    def __init__(self, parent=None, size=(1100, 700), offset=(0, 0), margin=12, settings=view_settings):
        self.settings = parent.settings
        super().__init__(parent)
        self.size = size
        self.setGeometry(offset[0], offset[1], size[0], size[1])
        self.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)

        # self.setContentsMargins(margin, margin, margin, margin)
        self.margin = margin
        # self.settings = settings
        self.update_settings()

    def update_settings(self):
        self.update_theme()

    def update_theme(self):
        self.setStyleSheet(f" border-radius: 10px;"
                           f" border: 3px solid {self.settings.color_theme.ACCENT_COLOR};"
                           f" margin: {self.margin}px;")

    def resizeEvent(self, event):
        self.size = event.size()
        self.setGeometry(0, 0, self.size.width(), self.size.height())

class CDivider(QtWidgets.QFrame):
    def __init__(self, parent=None, size=(700, 1), pos=(0, 0)):
        self.settings = parent.settings
        super().__init__(parent)
        self.size = size
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.update_settings()

    def update_settings(self):
        self.update_theme()

    def update_theme(self):
        self.setStyleSheet(f" border: 2px solid {self.settings.color_theme.SECONDARY_COLOR};")



class MainApplication(QtWidgets.QWidget):
    """Main view for the application"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = view_settings
        self.setMinimumSize(1100, 700)
        self.setWindowTitle("Main Application")
        self.setStyleSheet("background-color: #181818;")

        # Frame
        self.frame = CFrame(self)

        # Canvas
        self.canvas = CCanvas(self, pos=(40, 40), size=(670, 620))#(600, 400)

        # Point list
        self.list_view = CTableView(self, pos=(760, 40), size=(300, 535))

        self.divider = CDivider(self, pos=(734,40), size=(1, 620))

        # Buttons
        self.start_button = CButton(self, text="Start", pos=(760, 590), size=(300, 30))
        self.clear_button = CButton(self, text="Clear", pos=(760, 630), size=(300, 30))
        print(self.children())

    def set_theme(self, theme):
        self.canvas.update_theme()
        # self.list_view.set_theme(theme)
        self.start_button.update_theme()
        self.clear_button.update_theme()

    def resizeEvent(self, event):
        # self.canvas.resizeEvent(event)
        self.frame.resizeEvent(event)
