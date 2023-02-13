from __future__ import annotations
import numpy as np
from .point_helper import *


class Pattern:
    def __init__(self, matrix):
        self.matrix = matrix

    def txt(self) -> str:
        return matrix_to_txt(self.matrix)

    def size(self) -> (int, int):
        return len(self.matrix[0]), len(self.matrix)

    def create_snapshot(self, position: Point, size) -> Pattern:
        res = []
        for y in range(0, size[1]):
            if position.y + y < self.size()[1]:
                row = []
                for x in range(0, size[0]):
                    if position.x + x < self.size()[0]:
                        row.append(self.matrix[position.y + y][position.x + x])
                if 0 < len(row):
                    res.append(row)
        return Pattern(res)

    def rotate(self) -> Pattern:
        return Pattern(np.rot90(self.matrix))

    def mirror(self) -> Pattern:
        return Pattern(np.flip(self.matrix, 1))

    def find_matches(self, snapshot: Pattern):
        board = self.matrix
        matches = []

        def match_position(pos: Point, snapshot: Pattern):
            for y in range(0, snapshot.size()[1] - 1):
                for x in range(0, snapshot.size()[0] - 1):
                    cp = add_points(pos, Point(x, y))
                    if snapshot.matrix[y][x] not in ['0', '1']:
                        continue
                    if self.matrix[cp[1]][cp[0]] not in ['0', '1']:
                        continue
                    if snapshot.matrix[y][x] != self.matrix[cp[1]][cp[0]]:
                        return False
            return True

        for y in range(0, len(board) - snapshot.size()[1] - 1):
            for x in range(0, len(board[y]) - snapshot.size()[0] - 1):
                for r in (0, 90, 180, 270):
                    if match_position(Point(x, y), snapshot):
                        matches.append((Point(x, y), r))
                    snapshot = snapshot.rotate()

        return matches

    def matches_to_fields(self, snapshot: Pattern, board_size):
        return [((int(m[0][0] / 4 / (board_size / 10)), int(m[0][1] / 4 / (board_size / 10))), m[1]) for m in
                self.find_matches(snapshot)]


def matrix_to_txt(m):
    return '\n'.join([''.join(r) for r in m])


def txt_to_matrix(t):
    return [list(snr) for snr in t.split('\n') if len(snr) > 0]
