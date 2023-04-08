import cv2

from chessbots.lib.point_helper import Point, add_points


class DrawPoint:
    def __init__(self, pos: Point, radius: int, value: str, color: [int, int, int], fill: bool = False):
        self.pos = pos
        self.radius = radius
        self.value = value
        self.color = color
        self.fill = fill


class ImageHandler:
    def __init__(self, path: str):
        self.value_2 = 200 # this value can control noise in threshold work image
        self.alpha = 1# 1.7
        self.beta = 70
        self.path = path
        self.img = cv2.imread(path)

        self.thresh_black_bg_to_white = 230
        self.thresh_rest_bg_to_white = 40
        self.thresh_marker_to_bin = 140

    def get_work_img(self):
        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        img = 255 - img

        _, img = cv2.threshold(img, self.thresh_black_bg_to_white, 255, cv2.THRESH_TOZERO_INV)
        _, img = cv2.threshold(img, self.thresh_rest_bg_to_white, 255, cv2.THRESH_TOZERO)
        img = 255 - img
        _, img = cv2.threshold(img, self.thresh_marker_to_bin, 255, cv2.THRESH_BINARY)

        return img

    def write_work_img(self, filename: str):
        cv2.imwrite(filename, self.get_work_img())

    def draw_points(self, filename: str, points: [DrawPoint]):
        img = self.img.copy()
        for point in points:
            thickness = -1 if point.fill else 3
            cv2.circle(img, point.pos.raw, point.radius, point.color, thickness)
        for point in points: # in two goes, so pos is on top of circles
            cv2.putText(img, point.value, point.pos.add(Point(point.radius - 1, point.radius - 1)).raw, cv2.FONT_ITALIC, 0.4, (64, 64, 64))
            cv2.putText(img, point.value, point.pos.add(Point(point.radius - 2, point.radius - 2)).raw, cv2.FONT_ITALIC, 0.4, (198, 198, 198))

        cv2.imwrite(filename, img)
