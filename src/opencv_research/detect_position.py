import cv2
import numpy as np
import random
from matplotlib import pyplot as plt

def getPosition(imagePath):
    img = cv2.imread('images/' + imagePath)

    
    alignbars = findMatches(img, ['images/match_alignbars_white.png', 'images/match_alignbars_black.png'])
    zeros     = findMatches(img, ['images/match_zero_white.png',      'images/match_zero_black.png'])
    checks    = findMatches(img, ['images/match_check_white.png',     'images/match_check_black.png'])


    print(alignbars)

#    for bar in alignbars:
#        drawOutline(img, bar[0],bar[1],(240, 26, 2))
#
#    for bar in zeros:
#        drawOutline(img, bar[0],bar[1],(50, 62, 168))
#
#    for bar in checks:
#        drawOutline(img, bar[0],bar[1],(171, 201, 172))


    for alignbar in alignbars:
        barzeros = findMatchesByAlignbar(img, alignbar, zeros)
        barchecks = findMatchesByAlignbar(img, alignbar, checks)

        color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        for bar in barzeros:
            drawOutline(img, bar[0], bar[1], color)

        color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        for bar in barchecks:
            drawOutline(img, bar[0], bar[1], color)
        #print(len(barzeros) + len(barchecks))

    cv2.imwrite('out/' + imagePath, img)


def findMatchesByAlignbar(img, marker, matches):
    tolerance = 3
    field_size = img.shape[0] / 2
    markerOffset = [field_size / 4, field_size / 3] # <-- change here both to 4, when board_test.png updated..

    areaMin = [marker[0][0] - markerOffset[0], marker[0][1] - markerOffset[1]]
    areaMax = [areaMin[0] + field_size, areaMin[1] + field_size]

    filtered = []

    for match in matches:
        if(  
            match[0][0] > areaMin[0] - tolerance and
            match[0][1] > areaMin[1] - tolerance and
            match[1][0] < areaMax[0] + tolerance and
            match[1][1] < areaMax[1] + tolerance
        ):
          filtered.append(match)  
    return filtered


def findMatches(img, matchPaths):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    matches = []
    for matchPath in matchPaths:
        template = cv2.imread(matchPath,0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        
        for pt in zip(*loc[::-1]):
            #print(pt)
            match = (pt, (pt[0] + w, pt[1] + h))
            matches.append(match)

    return matches


def drawOutline(img, point1, point2, color):
    cv2.rectangle(img, point1, point2, color, 1)

    
getPosition('board_snippet_002.png')
#getPosition('board_snippet_004.png')
#getPosition('board_snippet_003.png')
#getPosition('board_snippet_004.png')