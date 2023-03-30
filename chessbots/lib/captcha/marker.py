import cv2
from chessbots.lib.point_helper import *


def in_tolerance(value, target: int, tolerance: int):
    return target - tolerance < value < target + tolerance


def not_negative(val: int | float):
    if 0 > val:
        return 0
    return val


class DummyMarker:
    def __init__(self, pos: Point):
        self.pos = pos
        self.radius = 0
        self.value = '2'


class Marker(DummyMarker):
    def __init__(self, contour, img):
        contours_poly = cv2.approxPolyDP(contour, 3, True)
        self.outer_range = [19, 3]  # target_radius, tolerance
        self.inner_range = [10, 3]  # target_radius, tolerance
        self.grid_size = 16
        center_tol = 5
        self.center_tolerance = [Point(-center_tol, -center_tol), Point(center_tol, center_tol)]
        self.box_tolerance = 2
        self.box = cv2.boundingRect(contours_poly)
        pos, radius = cv2.minEnclosingCircle(contours_poly)
        self.pos = Point(int(pos[0]), int(pos[1]))
        self.radius = int(radius)
        self.img = img
        self.value = '2'
        self.raw_center_circles = []
        self.center_circles = []
        self.valid_size = in_tolerance(self.radius, *self.outer_range)
        if self.valid_size:
            x1 = int(not_negative(self.pos.x - self.radius + self.box_tolerance))
            y1 = int(not_negative(self.pos.y - self.radius + self.box_tolerance))
            x2 = int(not_negative(self.pos.x + self.radius - self.box_tolerance))
            y2 = int(not_negative(self.pos.y + self.radius - self.box_tolerance))
            self.snapshot = self.img[y1:y2, x1:x2]
            # self.snapshot = self.img[self.box[1]:self.box[3], self.box[0]:self.box[2]]
            if 0 != len(self.snapshot):
                self.raw_center_circles = find_inner_markers(self.snapshot, self.radius)
                self.center_circles = [c for c in self.raw_center_circles if in_tolerance(c.radius, *self.inner_range)]
                self.center_circles = [c for c in self.raw_center_circles if
                                       point_in_area(sub_points(c.pos, Point(self.radius, self.radius)),
                                                     self.center_tolerance)]

            if 0 < len(self.center_circles):
                self.value = '0'
            if 0 == len(self.center_circles):
                self.value = '1'


class MarkerInner:
    def __init__(self, contour, original: int):
        self.tol = 4
        self.original = original
        contours_poly = cv2.approxPolyDP(contour, 3, True)
        self.box = cv2.boundingRect(contours_poly)
        pos, radius = cv2.minEnclosingCircle(contours_poly)
        self.pos = Point(int(pos[0]), int(pos[1]))
        self.radius = int(radius)


def find_contours(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    return contours


def find_inner_markers(img, original: int):
    return [MarkerInner(contour, original) for contour in find_contours(img)]


def find_markers(img):
    return [Marker(contour, img) for contour in find_contours(img)]


