from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QObject, Slot
from view.main_view import MainApplication
from model.graph import Graph
from controller.Thread import CThread
from model.point import PointsObject


class CCanvasController(QObject):
    refresh_signal = QtCore.Signal()

    def __init__(self, view, point_list=None):
        super().__init__()
        if point_list is None:
            point_list = []
        self.point_list = point_list
        self.view = view
        self.view.click_signal.connect(self.call_draw_point_signal_func)
        self.view.update_request.connect(self.refresh_request)
        self.path = []

    def refresh_request(self):
        self.refresh_signal.emit()

    @Slot(int, int)
    def call_draw_point_signal_func(self, x, y):
        if len(self.point_list.points) > 0:
            for point in self.point_list.points:
                if x in range(point.x - 5, point.x + 5) and y in range(point.y - 5, point.y + 5):
                    self.path = []
                    self.point_list.delete_point(point.id)
                    self.refresh_signal.emit()
                    return
        self.view.draw_point(x, y)
        self.point_list.add_point(x, y)
        self.refresh_signal.emit()

    def call_draw_points(self):
        for point in self.point_list.points:
            self.view.draw_point(point.x, point.y)

    def call_draw_path(self, path: list):
        if len(path) != len(self.point_list.points) + 1:
            return
        self.path = path
        for i in range(len(path)):
            first_point_index = self.get_point_index_by_id(path[i % len(path)])
            second_point_index = self.get_point_index_by_id(path[(i + 1) % len(path)])

            self.view.draw_path(self.point_list.points[first_point_index].x,
                                self.point_list.points[first_point_index].y,
                                self.point_list.points[second_point_index].x,
                                self.point_list.points[second_point_index].y)
        self.call_draw_points()

    def get_point_index_by_id(self, id_):
        for x in range(len(self.point_list.points)):
            if self.point_list.points[x].id == id_:
                return x

    def clear(self):
        self.point_list.points = []
        self.path = []
        self.refresh_signal.emit()
        self.refresh()

    def refresh(self):
        self.view.clear()
        self.call_draw_points()
        self.call_draw_path(self.path)


class CTableViewController(QObject):

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
        self.point_object = PointsObject()
        self.app = QtWidgets.QApplication([])
        self.main_app = MainApplication()
        self.canvas_controller = CCanvasController(self.main_app.canvas, self.point_object)
        self.table_controller = CTableViewController(self.main_app.list_view, self.point_object)
        self.thread = None

        for algorithm in self.ALGORITHMS:
            self.main_app.add_algorithm(algorithm)

        # Refresh signals
        self.canvas_controller.refresh_signal.connect(self.refresh)
        self.main_app.start_button.clicked.connect(self.start)  # self.greedy_solution)
        self.main_app.clear_button.clicked.connect(self.canvas_controller.clear)

    def run(self):
        """Runs the UI"""
        self.main_app.show()
        self.app.exec()

    @Slot()
    def refresh(self):
        self.table_controller.set_model()
        self.canvas_controller.refresh()

    def start(self):
        algorithm = self.main_app.radio_group.checked_button().text()
        self.thread = CThread(getattr(self, self.ALGORITHMS[algorithm]))
        self.thread.return_signal.connect(self.canvas_controller.call_draw_path)
        self.thread.start()

    def greedy_solution(self):
        if len(self.point_object.points) <= 1:
            return
        graph = Graph()
        graph.read_points(self.point_object.points)
        graph.solve_greedy()
        result = graph.get_result_ids()
        return result

    def brute_force_solution(self):
        if len(self.point_object.points) <= 1:
            return
        graph = Graph()
        graph.read_points(self.point_object.points)
        graph.solve_brute_force_start()
        result = graph.get_result_ids()
        return result
