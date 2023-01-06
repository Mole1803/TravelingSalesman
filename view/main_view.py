from random import random

#from PyQt6 import QtWidgets,QtGui,uic
#from PyQt6.QtQml import QQmlApplicationEngine
#from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu
#from PyQt6.QtCore import Qt





import sys

from PyQt6.QtCore import QStringListModel, QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickView


def run():
    app = QGuiApplication(sys.argv)
    data_list = ["hello", "world", "foo", "bar"]

    view = QQuickView()
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    my_model = QStringListModel()
    my_model.setStringList(data_list)
    view.setInitialProperties({"myModel": my_model})
    qml_file = "view/main.qml"
    view.setSource(QUrl.fromLocalFile(qml_file))

    view.show()

    #engine.load('view/main.qml')

    app.exec()
    del view



