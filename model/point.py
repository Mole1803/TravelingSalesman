from typing import Tuple


class PointsObject:
    def __init__(self):
        self.points: list[Point] = []
        self.config: Tuple[str, str, str] = ("id", "x", "y")

    def add_point(self, x, y):
        """Adds a point to the list of points, with the format (id, x, y)
        :param x: x coordinate of the point
        :param y: y coordinate of the point
        """
        self.points.append(Point(len(self.points), x, y))

    def delete_point(self, id_):
        """Deletes a point from the list of points
        :param id_: id of the point to be deleted
        """
        for i in range(len(self.points)):
            if self.points[i].id == id_:
                self.points.pop(i)
                break
        for i in range(len(self.points)):
            self.points[i] = Point(i, self.points[i].x, self.points[i].y)


class Point:
    def __init__(self, id_, x, y):
        self.id = id_
        self.x = x
        self.y = y
        self.config = {
            0: self.id,
            1: self.x,
            2: self.y
        }

    def id_to_attribute(self, index):
        return self.config[index]
