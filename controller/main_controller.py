from PyQt6.QtWidgets import QTableWidget
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QObject, Slot
from view.main_view import MainApplication
from model.graph import Graph


class PointsObject:
    def __init__(self):
        self.points = []
        self.config = ("id", "x", "y")

    def add_point(self, x, y):
        self.points.append((len(self.points),x,y))

class CCanvasController(QObject):
    refresh_signal = QtCore.Signal()
    def __init__(self, view, point_list=None):
        super().__init__()
        if point_list is None:
            point_list = []
        self.point_list = point_list
        self.view = view
        self.view.click_signal.connect(self.draw_point_signal_func)

    @Slot(int, int)
    def draw_point_signal_func(self, x, y):
        self.view.draw_point(x, y)
        self.point_list.add_point(x, y)
        self.refresh_signal.emit()
        print("x: " + str(x) + " y: " + str(y))

    def draw_points(self):
        for point in self.point_list.points:
            self.view.draw_point(point[1], point[2])

    def draw_path(self, path: list):
        self.view.clear()
        for i in range(len(path)):
            #print(path[i])
            first_point_index =path[i]
            second_point_index =path[i-1]
            self.view.draw_path(self.point_list.points[first_point_index][1],self.point_list.points[first_point_index][2],
                                self.point_list.points[second_point_index][1],self.point_list.points[second_point_index][2])

        self.draw_points()

    def clear(self):
        self.view.clear()
        self.point_list.points = []
        self.refresh_signal.emit()






class CTableView(QObject):
    def __init__(self, view, point_list=None):
        super().__init__()
        self.view = view
        self.point_list = point_list

    def set_model(self):
        self.view.set_model(self.point_list.points, self.point_list.config)



class MainController(QObject):
    def __init__(self):
        super().__init__()
        self.points = PointsObject()
        self.app = QtWidgets.QApplication([])
        self.mainApp = MainApplication()
        self.point_visualizer = CCanvasController(self.mainApp.canvas, self.points)
        self.point_config = CTableView(self.mainApp.list_view, self.points)

        # Refresh signals
        self.point_visualizer.refresh_signal.connect(self.refresh)
        self.mainApp.start_button.clicked.connect(self.greedy_solution)
        self.mainApp.clear_button.clicked.connect(self.point_visualizer.clear)


    def run(self):
        """Runs the UI"""
        self.mainApp.show()
        self.app.exec()


    @Slot()
    def refresh(self):
        #self.mainApp.list_view.model().layoutChanged.emit()
        print("refresh")
        print(self.points.points)
        self.point_config.set_model()

    def greedy_solution(self):
        if(len(self.points.points) == 0):
            return
        graph = Graph()
        graph.read_points(self.points.points)
        graph.create_nodes()
        graph.solve_greedy()
        result = graph.get_result_ids()
        self.point_visualizer.draw_path(result)


