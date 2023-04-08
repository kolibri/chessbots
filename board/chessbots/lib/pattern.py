from __future__ import annotations
import numpy as np
from .point_helper import *


class Pattern:
    def __init__(self, matrix):
        self.matrix = matrix

    def txt(self) -> str:
        return matrix_to_txt(self.matrix)

    def size(self) -> Point:
        return Point(len(self.matrix[0]), len(self.matrix))

    def create_snapshot(self, position: Point, size: Point) -> Pattern:
        res = []
        for y in range(0, size.y):
            if position.y + y < self.size().y:
                row = []
                for x in range(0, size.x):
                    if position.x + x < self.size().x:
                        row.append(self.matrix[position.y + y][position.x + x])
                if 0 < len(row):
                    res.append(row)
        return Pattern(res)

    def rotate(self) -> Pattern:
        return Pattern(np.rot90(self.matrix))

    def flip(self) -> Pattern:
        return Pattern(np.flip(self.matrix))

    def fliplr(self) -> Pattern:
        return Pattern(np.fliplr(self.matrix))

    def flipud(self) -> Pattern:
        return Pattern(np.flipud(self.matrix))

    def mirror(self) -> Pattern:
        return Pattern(np.flip(self.matrix, 1))

    def invert(self) -> Pattern:
        invert_txt = invert_zero_one(matrix_to_txt(self.matrix))
        return Pattern(txt_to_matrix(invert_txt))

    def bits(self, invert: bool = False) -> str:
        value = ''.join([''.join(r) for r in self.matrix])
        if invert:
            return value.replace('0', 'n').replace('1', '0').replace('n', '1')
        return value

    def find_matches(self, snapshot: Pattern):
        def match_position(pos: Point, snapshot: Pattern):
            check = self.create_snapshot(pos, snapshot.size())
            if check.txt() == snapshot.txt():
                return True
            return False

        board = self.matrix
        matches = []

        for y in range(0, len(board) - snapshot.size().y - 1):
            for x in range(0, len(board[y]) - snapshot.size().x - 1):
                if match_position(Point(x, y), snapshot):
                    matches.append((Point(x, y)))

        return matches

    def find_matches_old(self, snapshot: Pattern):
        board = self.matrix
        matches = []

        def match_position(pos: Point, snapshot: Pattern):
            for y in range(0, snapshot.size().y - 1):
                for x in range(0, snapshot.size().x - 1):
                    cp = add_points(pos, Point(x, y))
                    if snapshot.matrix[y][x] not in ['0', '1']:
                        continue
                    if self.matrix[cp.y][cp.x] not in ['0', '1']:
                        continue
                    if snapshot.matrix[y][x] != self.matrix[cp.y][cp.x]:
                        return False
            return True

        for y in range(0, len(board) - snapshot.size().y - 1):
            for x in range(0, len(board[y]) - snapshot.size().x - 1):
                for r in (0, 90, 180, 270):
                    if match_position(Point(x, y), snapshot):
                        matches.append((Point(x, y), r))
                    snapshot = snapshot.rotate()

        return matches

    # @todo: abandoned
    def matches_to_fields(self, snapshot: Pattern, board_size):
        return [((int(m[0][0] / 4 / (board_size / 10)), int(m[0][1] / 4 / (board_size / 10))), m[1]) for m in
                self.find_matches(snapshot)]


def matrix_to_txt(m):
    return '\n'.join([''.join(r) for r in m])


def txt_to_matrix(t):
    return [list(snr) for snr in t.split('\n') if len(snr) > 0]


def invert_zero_one(value: str):
    return value.replace('0', 'n').replace('1', '0').replace('n', '1')