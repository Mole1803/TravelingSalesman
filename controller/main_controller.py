from PyQt6.QtWidgets import QTableWidget
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QObject, Slot
from view.main_view import MainApplication
from model.graph import Graph
from controller.Thread import CThread, CWorker


class PointsObject:
    def __init__(self):
        self.points = []
        self.config = ("id", "x", "y")

    def add_point(self, x, y):
        """Adds a point to the list of points, with the format (id, x, y)
        :param x: x coordinate of the point
        :param y: y coordinate of the point
        """
        self.points.append((len(self.points),x,y))

    def delete_point(self, id):
        """Deletes a point from the list of points
        :param id: id of the point to be deleted
        """
        for i in range(len(self.points)):
            if self.points[i][0] == id:
                self.points.pop(i)
                break
        for i in range(len(self.points)):
            self.points[i] = (i, self.points[i][1], self.points[i][2])

class CCanvasController(QObject):
    refresh_signal = QtCore.Signal()
    def __init__(self, view, point_list=None):
        super().__init__()
        if point_list is None:
            point_list = []
        self.point_list = point_list
        self.view = view
        self.view.click_signal.connect(self.draw_point_signal_func)
        self.view.update_request.connect(self.refresh_request)
        self.path = []


    def refresh_request(self):
        self.refresh_signal.emit()

    @Slot(int, int)
    def draw_point_signal_func(self, x, y):
        if len(self.point_list.points)>0:
            for point in self.point_list.points:
                if x in range(point[1]-5,point[1]+5) and y in range(point[2]-5,point[2]+5):
                    #self.point_list.points.remove(point)
                    self.path = []
                    self.point_list.delete_point(point[0])
                    self.refresh_signal.emit()

                    #self.draw_points()
                    return
        self.view.draw_point(x, y)
        self.point_list.add_point(x, y)
        self.refresh_signal.emit()
        print("x: " + str(x) + " y: " + str(y))

    def draw_points(self):
        for point in self.point_list.points:
            self.view.draw_point(point[1], point[2])

    def draw_path(self, path: list):
        if len(path) != len(self.point_list.points)+1:
            return

        self.view.clear()
        self.path = path
        for i in range(len(path)):
            #print(path[i])
            first_point_index = self.getPointindexById(path[i%len(path)])
            second_point_index = self.getPointindexById(path[(i+1)%len(path)])

            self.view.draw_path(self.point_list.points[first_point_index][1],self.point_list.points[first_point_index][2],
                                self.point_list.points[second_point_index][1],self.point_list.points[second_point_index][2])

        self.draw_points()

    def getPointindexById(self,id):
        for x in range(len(self.point_list.points)):
            if self.point_list.points[x][0]==id:
                return x
    def clear(self):
        self.point_list.points = []
        self.path = []
        self.refresh_signal.emit()
        self.refresh()

    def refresh(self):
        self.view.clear()
        self.draw_points()
        self.draw_path(self.path)






class CTableView(QObject):
    def __init__(self, view, point_list=None):
        super().__init__()
        self.view = view
        self.point_list = point_list
        self.set_model()

    def set_model(self):
        self.view.set_model(self.point_list.points, self.point_list.config)



class MainController(QObject):
    ALGORITHMS = {
        "Greedy": "greedy_solution",
        "Brute Force": "brute_force_solution",
    }

    def __init__(self):
        super().__init__()
        self.points = PointsObject()
        self.app = QtWidgets.QApplication([])
        self.mainApp = MainApplication()
        self.point_visualizer = CCanvasController(self.mainApp.canvas, self.points)
        self.point_config = CTableView(self.mainApp.list_view, self.points)
        self.thread = None

        for algorithm in self.ALGORITHMS:
            self.mainApp.add_algorithm(algorithm)

        # Refresh signals
        self.point_visualizer.refresh_signal.connect(self.refresh)
        self.mainApp.start_button.clicked.connect(self.start)#self.greedy_solution)
        self.mainApp.clear_button.clicked.connect(self.point_visualizer.clear)


    def run(self):
        """Runs the UI"""
        self.mainApp.show()
        self.app.exec()


    @Slot()
    def refresh(self):
        #self.mainApp.list_view.model().layoutChanged.emit()
        self.point_config.set_model()
        self.point_visualizer.refresh()

    def start(self):
        algorithm = self.mainApp.radio_group.checked_button().text()
        print(algorithm)
        #getattr(self, self.ALGORITHMS[algorithm])()

        self.thread = CThread(getattr(self, self.ALGORITHMS[algorithm]))
        self.thread.return_signal.connect(self.draw_path)
        self.thread.start()



    def draw_path(self, path):
        self.point_visualizer.draw_path(path)



    def greedy_solution(self):
        if len(self.points.points) <= 1:
            return
        graph = Graph()
        graph.read_points(self.points.points)
        graph.create_nodes()
        graph.solve_greedy()
        result = graph.get_result_ids()
        return result

    def brute_force_solution(self):
        # TODO: Implement brute force solution
        graph = Graph()
        graph.read_points(self.points.points)
        graph.create_nodes()
        graph.solve_brute_force_start()
        result = graph.get_result_ids()
        return result


