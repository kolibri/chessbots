import math
import cv2
import numpy as np
from .Board import *


class Captcha:
    def __init__(self, img_path: str, templates: [[str, int]]):
        self.img_path = img_path
        self.img = cv2.imread(self.img_path)
        self.__templates = templates

    def resolve(self):
        angle = self.__calculate_angel()
        fixed_angle = abs(180 / angle[0] - 1) * 180
        return fixed_angle, self.__get_board()
        return angle[0], self.__get_board()

    def get_img_grid(self):
        grid = self.__find_grid()
        print([g[1][0] for g in grid])
        return self.__mark_positions([g[1][0] for g in grid])

    def get_img_matches(self):
        matches = self.__find_matches()
        return self.__mark_positions([g[0] for g in matches])

    def get_img_angle(self):
        degrees, angle = self.__calculate_angel()
        return self.__mark_positions(angle)

    def __get_board(self):
        txt = self.__get_txt_captcha()

        matrix = txt_to_matrix(txt)
        # fix matrix o_O
        # matrix = np.flip(matrix, 1)
        # matrix = np.flip(matrix, 0)

        return Board(matrix)

    # return: [degrees, [[a1_x, a1_y], [m_x, m_y], [a2_x, a2_y]]
    def __calculate_angel(self) -> [int, [[int, int], [int, int], [int, int]]]:
        def get_distance_to_center(pt: [int, int]) -> float:
            center = (int(self.img.shape[0] / 2), int(self.img.shape[1] / 2))
            return math.sqrt((center[0] - pt[0]) ** 2 + (center[1] - pt[1]) ** 2)

        def get_angle(a, b, c) -> [int, [[int, int], [int, int], [int, int]]]:
            ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
            return ang + 360 if ang < 0 else ang

        def get_matches_sorted_by_distance_to_center(matches):
            distances = [[get_distance_to_center(m[0]), m] for m in matches]
            sm = sorted(distances, key=lambda x: x[0])
            return [m[1] for m in sm]

        def angle_in_tolerance(point1, point2, point3):
            tolerance = 2
            return 90 - tolerance < get_angle(point1[0], point2[0], point3[0]) < 90 + tolerance

        matches = get_matches_sorted_by_distance_to_center(self.__find_matches())
        points = matches[0:3]
        angle_points = []
        if angle_in_tolerance(points[0], points[1], points[2]):
            angle_points = [points[0][0], points[1][0], points[2][0]]
        if angle_in_tolerance(points[1], points[2], points[0]):
            angle_points = [points[1][0], points[2][0], points[0][0]]
        if angle_in_tolerance(points[2], points[0], points[1]):
            angle_points = [points[2][0], points[0][0], points[1][0]]

        if angle_points:
            degrees = get_angle(angle_points[0], angle_points[1], (angle_points[0][1], angle_points[1][1]))
            return [degrees, angle_points]

        # todo: check another point, and so on
        return [None, []]

    def __find_matches(self) -> [[[int, int], int]]:  # [[img_x, img_y], marker]
        img = cv2.imread(self.img_path)
        # print('image', img, self.img_path, self.img)
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
                match = [[pt[0], pt[1]], tt[1]]
                matches.append(match)
        return matches

    def __find_grid(self) -> [[int, int], [int, int], int]:  # [[grid_x, grid_y], [img_x, img_y], marker]
        def check_for_point_or_create(point: [int, int], haystack: [[[int, int], int]]) -> [[int, int], int]:
            tolerance = 13
            for hay in haystack:
                area = [sub_points(point, [tolerance, tolerance]), add_points(point, [tolerance, tolerance])]
                if point_in_area(hay[0], area):
                    return hay
            return [point, 2]  # here we set the value for "not found"

        matches = self.__find_matches()
        degrees, angle = self.__calculate_angel()
        max_len = 16
        result = []
        for x in range(-max_len, max_len):
            for y in range(-max_len, max_len):
                mod_x = mult_point(sub_points(angle[1], angle[2]), x)
                mod_y = mult_point(sub_points(angle[1], angle[0]), y)
                expected_pos = add_points(angle[1], add_points(mod_x, mod_y))
                if self.img.shape[0] >= expected_pos[0] >= 0 and self.img.shape[1] >= expected_pos[1] >= 0:
                    result.append([[x, y], check_for_point_or_create(expected_pos, matches)])
        return result

    def __get_txt_captcha(self):
        grid = self.__find_grid()
        grid = [g for g in grid if g[1][1] in [1, 0]]

        max_x = max([g[0][0] for g in grid]) + 1
        max_y = max([g[0][1] for g in grid]) + 1
        min_x = min([g[0][0] for g in grid])
        min_y = min([g[0][1] for g in grid])

        res = ''
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if [x, y] in [g[0] for g in grid]:
                    index = [g[0] for g in grid].index([x, y])
                    cell = grid[index]
                    res = res + str(cell[1][1])
                else:
                    res = res + '2'
            res = res + '\n'
        return res

    def __mark_positions(self, pos: [[int, int]]):
        img = cv2.imread(self.img_path)  # create new image
        color = (255, 0, 255)
        for p in pos:
            print(p)
            # img = cv2.rectangle(img, sub_points(p, [3, 3]), add_points(p, [3, 3]), color, 2)
            # todo: cv2.rectangle should work with (img, p1, p2, ...) according to docs o_O
            # todo: but without, color is wrong...
            img = cv2.rectangle(
                img,
                [list(sub_points(p, [3, 3])), list(add_points(p, [3, 3]))],
                list(color),
                2
            )

        return img

