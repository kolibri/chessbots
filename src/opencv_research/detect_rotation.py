import math
import time
import cv2
import numpy as np
import random
from matplotlib import pyplot as plt


def draw_outline(img, point1, point2, color):
    cv2.rectangle(img, point1, point2, color, 1)


def find_matches(img, match_paths):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    matches = []
    for match_path in match_paths:
        template = cv2.imread(match_path, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            # print(pt)
            match = (pt, (pt[0] + w, pt[1] + h))
            matches.append(match)
    #print(matches)
    return matches


img = cv2.imread('images/rotation_base.png')
matches = find_matches(img, [
    'images/pattern_WO.png',
    'images/pattern_WX.png',
    'images/pattern_BO.png',
    'images/pattern_BX.png',
])


for match in matches:
    print(match)
    draw_outline(img, match[0], match[1], (123, 123, 123))


cv2.imwrite('images/rotation_out.png', img)
