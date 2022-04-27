import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('images/board_test.png')

cw = int(img.shape[0] / 10) * 2
ch = int(img.shape[0] / 10) * 2


def createCrop(x, y):
    return img[y:y + ch, x:x + cw]


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


cv2.imwrite('images/position_image02.png', createCrop(0, 0))
cv2.imwrite('images/position_image04.png', createCrop(cw * 2, cw * 3))
cv2.imwrite(
    'images/position_image03.png',
    createCrop(
        img.shape[0] - int(img.shape[0] / 3),
        img.shape[1] - int(img.shape[0] / 5),
    )
)

img = rotate_image(img, 71)
cv2.imwrite('images/board_snippet_004.png', createCrop(int(cw * 2.2), int(cw * 3.7)))
