import cv2

from chessbots.lib.point_helper import *
from typing import NamedTuple


class Circle(NamedTuple):
    pos: Point
    radius: int

    def is_inside(self, other: Self) -> bool:
        d = abs(other.pos.distance(self.pos))
        tol = other.radius - self.radius
        # print('ii', self.pos.txt, self.radius, other.pos.txt, other.radius, d, tol, d < tol)
        return d < tol


def find_circles(img_thresh) -> [Circle]:
    contours, _ = cv2.findContours(image=img_thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    return [contour_to_circle(c) for c in contours]


def contour_to_circle(contour) -> Circle:
    contours_poly = cv2.approxPolyDP(contour, 3, True)
    pos, radius = cv2.minEnclosingCircle(contours_poly)
    return Circle(
        Point(int(pos[0]), int(pos[1])),
        int(radius)
    )


class Marker(NamedTuple):
    pos: Point
    radius: int
    value: str


def find_inner_circles_for_value(outer: Circle, inners: [Circle]):
    inner_circles = [i for i in inners if i.is_inside(outer)]
    # mindfuck: 0 found circles mean a dot ('1'). found inner circles mean a cirlce ('0').
    value = '0' if 0 < len(inner_circles) else '1'
    return value, inner_circles


class MarkerResult:
    def __init__(self, img, min_o: int, max_o: int, min_i: int, max_i: int):
        self.noise_filter_minimal_radius = 6
        self.min_o = min_o
        self.max_o = max_o
        self.min_i = min_i
        self.max_i = max_i

        self.img_thresh = img
        self.raw_contours_pos_angle = find_circles(self.img_thresh)
        self.raw_contours_pos_angle = [r for r in self.raw_contours_pos_angle if r.radius > 0] # just for debugging pictures
        self.filtered_contours = [c for c in self.raw_contours_pos_angle if self.min_i <= c.radius <= self.max_o]
        self.outer_shells = [c for c in self.filtered_contours if self.min_o <= c.radius <= self.max_o]
        self.inner_shells = [c for c in self.filtered_contours if self.min_i <= c.radius <= self.max_i]
        self.raw_markers = [[c, find_inner_circles_for_value(c, self.inner_shells)] for c in self.outer_shells]
        self.markers = [Marker(c.pos, c.radius, vic[0]) for c, vic in self.raw_markers]


