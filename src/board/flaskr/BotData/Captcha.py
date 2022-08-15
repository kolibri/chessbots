import math
import cv2
from .Board import *


def in_tolerance(value, target: int, tolerance: int):
    return target - tolerance < value < target + tolerance


class AngelCalculator:
    @staticmethod
    def get_angle(a: PointImg, b: PointImg, c: PointImg) -> float:
        ang = math.degrees(math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x))
        return ang + 360 if ang < 0 else ang

    @staticmethod
    def find_angel_points(markers: [[PointImg, int]]) -> [PointImg, PointImg, PointImg]:
        # sort by distance, return the first three PointImg only
        sm = sorted(markers, key=lambda x: x[2])
        sm = sm[0:3]
        points = [m[0] for m in sm]
        # return in the right order, center of 90° in the middle
        if in_tolerance(AngelCalculator.get_angle(points[0], points[1], points[2]), 90, 2):
            return [points[0], points[1], points[2]]
        if in_tolerance(AngelCalculator.get_angle(points[1], points[2], points[0]), 90, 2):
            return [points[1], points[2], points[0]]
        if in_tolerance(AngelCalculator.get_angle(points[2], points[0], points[1]), 90, 2):
            return [points[2], points[0], points[1]]
        raise RuntimeError('Could not find three dots with 90 degree angle o_O')


class MarkerFinder:
    def __init__(self, templates: [[str, int]]):
        self.__templates = templates

    def find_markers(self, img) -> [[PointImg, int, float, Point]]:  # foundAt, marker, distance, size
        center = mult_point(PointImg(img.shape[0], img.shape[1]), 0.5)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        matches = []
        for tt in self.__templates:
            template = cv2.imread(tt[0], 0)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):
                # p1, p2, mark, distance to center
                p = PointImg(pt[0], pt[1])
                matches.append([
                    p,
                    tt[1],
                    math.sqrt((center.x - p.x) ** 2 + (center.y - p.y) ** 2)
                ])
        return MarkerFinder.filter_overlapping(matches, [])

    @staticmethod
    def filter_overlapping(
            markers: [[PointImg, int, float, Point]],
            carry: [[PointImg, int, float, Point]] = []
    ) -> [
        [PointImg, int, float, Point]
    ]:
        if not markers:
            return carry
        tol_p = PointImg(5, 5)
        current = markers.pop(0)
        area = PointImg(sub_points(current[0], tol_p), add_points(current[0], tol_p))
        carry.append(current)
        markers_new = [m for m in markers if not point_in_area(m[0], area)]
        return MarkerFinder.filter_overlapping(markers_new, carry)


class GridResolver:
    @staticmethod
    def resolve_grid(markers: [[PointImg, int]], area_max: PointImg) -> [[PointGrid, [PointImg, int]]]:
        def create_grid_point(point: PointImg, haystack: [[PointImg, int]]) -> [PointImg, int]:
            tol_point = PointImg(13, 13)
            for hay in haystack:
                area = [sub_points(point, tol_point), add_points(point, tol_point)]
                if point_in_area(hay[0], area):
                    return hay
            return [point, 2]  # here we set the value for "not found"

        # this might be not so good, as we did not check for the middle angle(?)
        angle = AngelCalculator.find_angel_points(markers)
        grid_max = 16
        result = []
        print('hereee', angle, area_max, '#', abs_point(sub_points(angle[1], angle[2])),
              abs_point(sub_points(angle[1], angle[0])), markers)
        for x in range(-grid_max, grid_max):
            for y in range(-grid_max, grid_max):
                mod_x = mult_point(abs_point(sub_points(angle[1], angle[2])), x)
                mod_y = mult_point(abs_point(sub_points(angle[1], angle[0])), y)
                expected_pos = add_points(angle[1], add_points(mod_x, mod_y))
                if area_max.x >= expected_pos.x >= 0 and area_max.y >= expected_pos.y >= 0:
                    result.append([PointGrid(x, y), create_grid_point(expected_pos, markers), expected_pos])
        return result

    @staticmethod
    def grid_to_txt(grid: [[PointGrid, [PointImg, int]]]):
        grid = [g for g in grid if g[1][1] in [1, 0]]

        max_x = max([g[0].x for g in grid]) + 1
        max_y = max([g[0].y for g in grid]) + 1
        min_x = min([g[0].x for g in grid])
        min_y = min([g[0].y for g in grid])

        res = ''
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if PointGrid(x, y) in [g[0] for g in grid]:
                    index = [g[0] for g in grid].index(PointGrid(x, y))
                    cell = grid[index]
                    res = res + str(cell[1][1])
                else:
                    # print('TWO', PointGrid(x, y), max_x, max_y, min_x, min_y, grid )
                    res = res + '2'
            res = res + '\n'
        return res


class Captcha:
    def __init__(self, img_path: str, templates: [[str, int]]):
        self.img_path = img_path
        self.img = cv2.imread(self.img_path)
        self.__templates = templates
        self.finder = MarkerFinder(self.__templates)

    # this gives the angel of the captcha, ignoring rotation
    # you need to add this to the rotation result from board
    def get_captcha_angel(self) -> float:
        markers = self.finder.find_markers(self.img)
        angle_points = AngelCalculator.find_angel_points(markers)
        angle = AngelCalculator.get_angle(*angle_points)
        return angle % 90

    def get_board(self) -> Board:
        markers = self.finder.find_markers(self.img)
        grid_txt = GridResolver.grid_to_txt(GridResolver.resolve_grid(markers, PointImg(self.img.shape[0], self.img.shape[1])))
        return Board(txt_to_matrix(grid_txt))

    # def __mark_positions(self, pos: [PointImg]):
    #     img = cv2.imread(self.img_path)  # create new image
    #     color = (255, 0, 255)
    #     for p in pos:
    #         print(p)
    #         # img = cv2.rectangle(img, sub_points(p, [3, 3]), add_points(p, [3, 3]), color, 2)
    #         # todo: cv2.rectangle should work with (img, p1, p2, ...) according to docs o_O
    #         # todo: but without, color is wrong...
    #         img = cv2.rectangle(
    #             img,
    #             [list(sub_points(p, [3, 3])), list(add_points(p, [3, 3]))],
    #             list(color),
    #             2
    #         )
    #
    #     return img
