import math
import cv2
import numpy as np


from .PointHelper import *


def draw_outline(img, point1: [int, int], point2: [int, int], color):
    cv2.rectangle(img, point1, point2, tuple (color), 1)


class Captcha:
    def __init__(self, img_path: str, templates: [[str, int]]):
        self.img_path = img_path
        self.__templates = templates

    # return: [degrees, [[a1_x, a1_y], [m_x, m_y], [a2_x, a2_y]]
    def calculate_angel(self) -> [int, [[int, int], [int, int], [int, int]]]:
        img = cv2.imread(self.img_path)
        matches = self.find_matches()
        t = 2

        def get_distance_to_center(pt: [int, int]) -> float:
            center = (int(img.shape[0] / 2), int(img.shape[1] / 2))
            return math.sqrt((center[0] - pt[0]) ** 2 + (center[1] - pt[1]) ** 2)

        def find_nearest_matches(matches: [[[int, int], int]], point: [int, int], limit: int) -> [[[int, int], int]]:
            found = []
            for x in range(0, img.shape[0]):
                for match in matches:
                    if point_in_area(match[0], [point[0], add_points(point[0], [x, x])]):
                        if match not in found:
                            found.append(match)
                            if len(found) >= limit:
                                return found
            return found  # todo: exception handling

        def get_angle(a, b, c) -> [int, [[int, int], [int, int], [int, int]]]:
            ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
            return ang + 360 if ang < 0 else ang

        distances = [get_distance_to_center(m[0]) for m in matches]
        center_point = matches.pop(distances.index(min(distances)))
        points = find_nearest_matches(matches, center_point, 2)
        points.append(center_point)
        angle_points = []
        #print(points)
        if 90 - t < get_angle(points[0][0], points[1][0], points[2][0]) < 90 + t:
            angle_points = [points[0][0], points[1][0], points[2][0]]
        if 90 - t < get_angle(points[1][0], points[2][0], points[0][0]) < 90 + t:
            angle_points = [points[1][0], points[2][0], points[0][0]]
        if 90 - t < get_angle(points[2][0], points[0][0], points[1][0]) < 90 + t:
            angle_points = [points[2][0], points[0][0], points[1][0]]

        if angle_points:
            degrees = get_angle(angle_points[0], angle_points[1], (angle_points[0][1], angle_points[1][1]))
            return [degrees, angle_points]

        # todo: check another point, and so on
        return [None, []]

    def find_matches(self) -> [[[int, int], int]]:  # [[img_x, img_y], marker]
        print(self.img_path, self.__templates)
        img = cv2.imread(self.img_path)
        print(img)
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
                match = ([pt[0], pt[1]], tt[1])
                matches.append(match)
        return matches

    def find_grid(self) -> [[int, int], [int, int], int]:  # [[grid_x, grid_y], [img_x, img_y], marker]

        def find_at_point(point: [int, int], haystack: [[[int, int], int]], tolerance: int) -> [[int, int], int]:
            for hay in haystack:
                area = [sub_points(point, [tolerance, tolerance]), add_points(point, [tolerance, tolerance])]
                if point_in_area(hay[0], area):
                    return hay
            return [point, 2]  # here we set the value for "not found"

        matches = self.find_matches()
        degrees, angle = self.calculate_angel()
        max_len = 10
        t = 12
        mod_x = sub_points(angle[1], angle[0])
        mod_y = sub_points(angle[1], angle[2])
        result = []
        reference = angle[1]
        for x in range(-max_len, max_len):
            for y in range(-max_len, max_len):
                mx = mult_point(mod_x, x)
                my = mult_point(mod_y, y)
                m = add_points(mx, my)
                mp = add_points(reference, m)
                if mp[0] > 0 and mp[1] > 0:
                    result.append([[x, y], find_at_point(mp, matches, t)])
        return result

    def get_txt_captcha(self):
        grid = self.find_grid()
        #print('grid', grid)
        grid = [g for g in grid if g[1][1] in [1, 0]]

        max_x = max([g[0][0] for g in grid])
        max_y = max([g[0][1] for g in grid])
        min_x = min([g[0][0] for g in grid])
        min_y = min([g[0][1] for g in grid])

        res = ''
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if [x,y] in [g[0] for g in grid]:
                    index = [g[0] for g in grid].index([x,y])
                    cell = grid[index]
                    # print([x,y], index, cell)
                    #res = res + str(cell[1][1])
                    if 1 == cell[1][1]:
                        res = res + 'X'
                    elif 0 == cell[1][1]:
                        res = res + '0'
                    elif 2 == cell[1][1]:
                        res = res + '.'
                    else:
                        res = res + '?'
                else:
                    res = res + ' '
            res = res + '\n'
        return res

    def get_img_grid(self):
        grid = self.find_grid()
        img = cv2.imread(self.img_path)
        for g in grid:
            t = 12
            p1 = sub_points(g[1][0], [t, t])
            p2 = add_points(g[1][0], [t, t])
            color = (0, 0, 255)
            if g[1][1] == 0:
                color = (255, 0, 0)
            if g[1][1] == 1:
                color = (0, 255, 0)
            img = cv2.rectangle(img, p1, p2, color, 1)
            text = str(g[0][0]) + 'x' + str(g[0][1])
            img = cv2.putText(img, text, add_points(p1, [1,8]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1, cv2.LINE_AA)

        return img

    def get_img_matches(self):
        matches = self.find_matches()
        img = cv2.imread(self.img_path)
        for g in matches:
            t = 2
            p1 = sub_points(g[0], [t, t])
            p2 = add_points(g[0], [t, t])
            color = (0, 0, 255)
            if g[1] == 0:
                color = (255, 0, 0)
            if g[1] == 1:
                color = (0, 255, 0)
            img = cv2.rectangle(img, [p1, p2], tuple(color), 1)
        return img

    def get_img_angle(self):
        degrees, angle = self.calculate_angel()
        img = cv2.imread(self.img_path)
        for g in angle:
            t = 2
            p1 = sub_points(g, [t, t])
            p2 = add_points(g, [t, t])
            color = (0, 0, 255)
            img = cv2.rectangle(img, p1, p2, color, 1)
        return img
