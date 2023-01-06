from PyQt6 import QtWidgets,QtGui,uic
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtQml import QQmlApplicationEngine


class MainApplication(QtWidgets.QWidget):
    """Main view for the application"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 800)

        # Some random stuff
        self.parent_size = self.frameGeometry().size()
        print(self.parent_size)

        # A canvas to draw on
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(800, 600)
        canvas.fill(QtGui.QColor("green"))
        self.label.setPixmap(canvas)


        # Empty sidebar for configrations
        self.empty_widget = QtWidgets.QWidget()
        self.setMinimumSize(800, 200)

        # Layouts
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.empty_widget)

        self.setLayout(self.layout)


def run():
    """Runs the UI"""
    app = QtWidgets.QApplication([])
    window = MainApplication()
    window.show()
    app.exec()