import typing
from functools import partial

from PyQt6.QtWidgets import QToolBar
from PySide6.QtCore import QObject
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QListView, QTableView, QTableWidget
from PySide6.QtGui import QBrush, QColor, QPen
from view.properties import Settings, CColor, CColorTheme

view_settings = Settings()


class CCanvas(QtWidgets.QGraphicsView):
    click_signal = QtCore.Signal(int, int)
    background_color = None
    update_request = QtCore.Signal()

    def __init__(self, parent=None, size=(600, 400), pos=(25, 25), point_radius=6, settings=view_settings):
        super().__init__(parent)
        self.inital_size = size
        # Setup scene
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        # Sizing
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setMinimumSize(size[0], size[1])
        # self.setMaximumSize(size[0], size[1])
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

        self.resize_func = None

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() != QtCore.Qt.MouseButton.LeftButton:
            return
        points = self.mapToScene(event.pos())
        pos_x = int((points.x() * self.inital_size[0]) / self.width())
        pos_y = int((points.y() * self.inital_size[1]) / self.height())
        valid_x = 0 <= pos_x <= self.width()
        valid_y = 0 <= pos_y <= self.height()
        if not valid_x or not valid_y:
            return

        self.click_signal.emit(pos_x, pos_y)

    def draw_point(self, x: int, y: int, point_color: str = None) -> None:
        """Draws a point on the canvas
        Args:
            x (int): x coordinate of point
            y (int): y coordinate of point
            point_color (str, optional): Color of path in hex. Defaults to None.
        """
        if point_color is None:
            point_color = self.settings.color_theme.CANVAS_POINT_COLOR
        x = int((x * self.width()) / self.inital_size[0])
        y = int((y * self.height()) / self.inital_size[1])
        self.scene.addEllipse(x - (self.point_radius / 2.0), y - (self.point_radius / 2.0), self.point_radius,
                              self.point_radius,
                              pen=QtGui.QPen(QtGui.QColor(point_color), self.point_radius))

    def draw_path(self, x_1: int, y_1: int, x_2: int, y_2: int, path_color: str = None) -> None:
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
        x_1 = int((x_1 * self.width()) / self.inital_size[0])
        y_1 = int((y_1 * self.height()) / self.inital_size[1])
        x_2 = int((x_2 * self.width()) / self.inital_size[0])
        y_2 = int((y_2 * self.height()) / self.inital_size[1])

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

    def c_resize(self):
        """Resizes the canvas to the size of the parent widget"""
        x, y, w, h = self.resize_func()
        self.setGeometry(x, y, w, h)
        self.setSceneRect(0, 0, w, h)
        self.update_request.emit()


class CTableWidget(QtCore.QAbstractTableModel):
    def __init__(self, data, headers=None, parent=None, settings=view_settings):
        super().__init__(parent)
        self._data = data
        self._headers = headers
        self.settings = settings

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        # center text
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        if role == QtCore.Qt.ItemDataRole.ForegroundRole:
            return QtGui.QColor(self.settings.color_theme.TABLE_TEXT_COLOR)

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
    def __init__(self, parent=None, size=(300, 550), pos=(0, 0), margin_right=0, margin_top=0, margin_bottom=0):
        super().__init__(parent)

        self.settings = parent.settings

        self.setMinimumSize(size[0], size[1])
        # self.setMaximumSize(size[0], size[1])

        self.setGeometry(pos[0], pos[1], size[0], size[1])

        self.model = None
        # disable vertical header
        self.verticalHeader().setVisible(False)
        # horizontal header
        self.horizontalScrollBar().setDisabled(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.margin_right = margin_right
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom

        self.update_settings()
        self.resize_func = None

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

    def c_resize(self):
        x, y, size_x, size_y = self.resize_func()
        self.setGeometry(x, y, size_x, size_y)



class CButton(QtWidgets.QPushButton):
    theme = None

    def __init__(self, parent=None, text="Button", size=(100, 30), pos=(0, 0), settings=view_settings):
        super().__init__(parent)
        self.setMinimumSize(size[0], size[1])
        self.setMaximumSize(size[0], size[1])
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setText(text)

        self.settings = settings
        self.resize_func = None

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

    def c_resize(self):
        x, y, size_x, size_y = self.resize_func()
        self.setGeometry(x, y, size_x, size_y)


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
    def __init__(self, parent=None, size=(700, 1), pos=(0, 0), margin_top=0, margin_bottom=0, margin_left=0,
                 margin_right=0):
        self.settings = parent.settings
        super().__init__(parent)
        # self.size = size
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)

        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right

        self.update_settings()
        self.resize_func = None

    def update_settings(self):
        self.update_theme()

    def update_theme(self):
        self.setStyleSheet(f" border: 2px solid {self.settings.color_theme.SECONDARY_COLOR};")

    def c_resize(self):
        x, y, size_x, size_y = self.resize_func()
        self.setGeometry(x, y, size_x, size_y)


class CRadioButton(QtWidgets.QRadioButton):
    def __init__(self, parent=None, text="Button", size=(100, 30), pos=(0, 0)):
        super().__init__(parent)
        self.setMinimumSize(size[0], size[1])
        self.setMaximumSize(size[0], size[1])
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.setText(text)

        self.settings = parent.settings
        self.update_settings()

    def update_settings(self):
        self.update_theme()

    def update_theme(self):
        self.setStyleSheet("QRadioButton {"
                           f"background-color: {self.settings.color_theme.BACKGROUND_COLOR};"
                           f" border: 0px solid transparent;"
                           f" color: {self.settings.color_theme.LIGHT_TEXT_COLOR};"
                           f" font-weight: bold;"
                           f" border-radius: 5px;"
                           "}"

                           "QRadioButton:hover {"
                           f" border: 1px solid {self.settings.color_theme.ON_HOVER_COLOR};"
                           "}")


class CRadioGroup(QtWidgets.QGroupBox):
    algorithm = QtCore.Signal(str)

    def __init__(self, parent=None, size=(100, 30), pos=(0, 0), ):
        super().__init__(parent)
        self.setMinimumSize(size[0], size[1])
        self.setMaximumSize(size[0], size[1])
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.settings = parent.settings

        self.resize_func = None

        self.update_settings()

    def add_radio_button(self, text):
        radio_button = CRadioButton(self, text=text)
        self.layout.addWidget(radio_button)
        # if more than one radio button is added, check the first one
        if self.layout.count() > 1:
            self.layout.itemAt(0).widget().setChecked(True)

    def checked_button(self):
        for i in range(self.layout.count()):
            if self.layout.itemAt(i).widget().isChecked():
                return self.layout.itemAt(i).widget()

    def update_settings(self):
        self.update_theme()

    def update_theme(self):
        self.setStyleSheet("QGroupBox {"
                           f"background-color: {self.settings.color_theme.BACKGROUND_COLOR};"
                           f" border: 0px solid transparent;"
                           f" color: {self.settings.color_theme.LIGHT_TEXT_COLOR};"
                           f" font-weight: bold;"
                           f" border-radius: 5px;"
                           "}"

                           "QGroupBox:hover {"
                           f" border: 1px solid {self.settings.color_theme.ON_HOVER_COLOR};"
                           "}")

    def c_resize(self):
        x, y, size_x, size_y = self.resize_func()
        self.setGeometry(x, y, size_x, size_y)


class CMenu(QtWidgets.QMenu):
    def __init__(self, parent=None, text="Menu"):
        super().__init__(parent)
        self.setTitle(text)
        self.addAction("New")


class CMenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = view_settings
        self.addMenu(CMenu(self, text="&File"))
        self.setStyleSheet(f"background-color: {self.settings.color_theme.ACCENT_COLOR};"
                           f"selection-color:{self.settings.color_theme.CANVAS_PATH_COLOR};"
                           f"selection-background-color: {self.settings.color_theme.ON_HOVER_COLOR};"
                           f"border-radius: 0px")


class MainApplication(QtWidgets.QWidget):
    """Main view for the application"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = view_settings
        self.setMinimumSize(1100, 700)
        self.setWindowTitle("Traveling Salesman")
        self.setStyleSheet(f"background-color: {self.settings.color_theme.SHEET_COLOR}")
        try:
            self.setWindowIcon(QtGui.QIcon(view_settings.APP_ICON_PATH))
        except:
            pass

        # Margins
        self.margin_top = 40
        self.margin_bottom = self.margin_top
        self.margin_left = self.margin_top
        self.margin_right = self.margin_top

        # Frame
        self.frame = CFrame(self)

        # Canvas

        self.canvas = CCanvas(self, pos=(self.margin_top, self.margin_right), size=(670, 620))
        self.canvas.resize_func = self.calculate_canvas_geometry

        # Point list
        self.list_view_width = 300
        self.list_view_height = 400

        self.list_view_initial_x = self.size().width() - self.list_view_width - self.margin_right
        self.list_view_initial_y = self.margin_top

        self.list_view = CTableView(self, pos=(self.list_view_initial_x, self.list_view_initial_y),
                                    size=(self.list_view_width, self.list_view_height), margin_top=self.margin_top,
                                    margin_right=self.margin_right)

        # sets a custom resize function for the table view
        self.list_view.resize_func = self.calculate_table_geometry

        # Divider
        self.divider_width = 1
        self.divider_height = self.size().height() - self.margin_top - self.margin_bottom

        self.margin_list_view_divider = 26
        self.divider_initial_x = self.list_view_initial_x - self.margin_list_view_divider

        self.divider_margin_right = self.size().width() - self.divider_initial_x

        self.divider = CDivider(self, pos=(self.divider_initial_x, self.margin_top),
                                size=(self.divider_width, self.divider_height), margin_top=self.margin_top,
                                margin_right=self.divider_margin_right, margin_bottom=self.margin_bottom)
        self.divider.resize_func = self.calculate_divider_geometry

        # self.setFixedSize(self.size())

        # Buttons
        self.button_size_x = 300
        self.button_size_y = 30
        self.size_between_buttons = 40
        self.start_button = CButton(self, text="Start", pos=(760, 590), size=(self.button_size_x, self.button_size_y))
        self.start_button.resize_func = self.calculate_start_button_geometry
        self.clear_button = CButton(self, text="Clear", pos=(760, 630), size=(self.button_size_x, self.button_size_y))
        self.clear_button.resize_func = self.calculate_clear_button_geometry

        # Radio group
        self.radio_group_pos_y = self.size().height() - self.margin_bottom - self.button_size_y * 2 - self.size_between_buttons * 2
        self.radio_group = CRadioGroup(self, pos=(760, 460), size=(150, 100))
        self.radio_group.resize_func = self.calculate_radio_group_geometry
        # self.menu = CMenuBar(self)

    def set_theme(self, theme):
        self.canvas.update_theme()
        self.list_view.update_theme()
        self.radio_group.update_theme()
        # self.list_view.set_theme(theme)
        self.start_button.update_theme()
        self.clear_button.update_theme()

    def resizeEvent(self, event):
        # self.canvas.resizeEvent(event)
        self.frame.resizeEvent(event)

        self.divider.c_resize()
        self.start_button.c_resize()
        self.clear_button.c_resize()
        self.radio_group.c_resize()
        self.list_view.c_resize()
        self.canvas.c_resize()

    def add_algorithm(self, algorithm):
        self.radio_group.add_radio_button(algorithm)

    def calculate_table_geometry(self):
        x = self.size().width() - self.list_view_width - self.margin_right
        y = self.margin_top
        w = self.list_view_width
        h = self.size().height() - self.radio_group.size().height() - self.margin_bottom - self.size_between_buttons * 2 - self.start_button.size().height() - self.clear_button.size().height() - 10
        return x, y, w, h

    def calculate_divider_geometry(self):
        x = self.size().width() - self.list_view_width - self.margin_right - self.margin_list_view_divider
        y = self.margin_top
        w = self.divider_width
        h = self.size().height() - self.margin_top - self.margin_bottom
        return x, y, w, h

    def calculate_canvas_geometry(self):
        x = self.margin_top
        y = self.margin_right
        w = self.size().width() - self.list_view_width - self.margin_right - self.margin_left - self.margin_list_view_divider * 2 - self.divider_width
        h = self.size().height() - self.margin_top - self.margin_bottom
        return x, y, w, h

    def calculate_start_button_geometry(self):

        x = self.size().width() - self.start_button.size().width() - self.margin_right
        y = self.size().height() - self.start_button.size().height() - self.margin_bottom - self.size_between_buttons
        w = self.start_button.size().width()
        h = self.start_button.size().height()
        return x, y, w, h

    def calculate_clear_button_geometry(self):
        x = self.size().width() - self.clear_button.size().width() - self.margin_right
        y = self.size().height() - self.clear_button.size().height() - self.margin_bottom
        w = self.clear_button.size().width()
        h = self.clear_button.size().height()
        return x, y, w, h

    def calculate_radio_group_geometry(self):
        x = self.size().width() - self.radio_group.size().width() * 2 - self.margin_right
        y = self.size().height() - self.radio_group.size().height() - self.margin_bottom - self.size_between_buttons - self.start_button.size().height() - self.clear_button.size().height()
        w = self.radio_group.size().width()
        h = self.radio_group.size().height()
        return x, y, w, h
