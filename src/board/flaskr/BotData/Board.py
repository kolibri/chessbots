from __future__ import annotations
import numpy as np
from .PointHelper import *


class Board:
    def __init__(self, matrix):
        self.matrix = matrix

    def txt(self) -> str:
        return matrix_to_txt(self.matrix)

    def size(self) -> (int, int):
        return len(self.matrix[0]), len(self.matrix)

    def create_snapshot(self, position, size) -> Board:
        res = []
        for y in range(0, size[1]):
            if position[1] + y < self.size()[1]:
                row = []
                for x in range(0, size[0]):
                    if position[0] + x < self.size()[0]:
                        row.append(self.matrix[position[1] + y][position[0] + x])
                if 0 < len(row):
                    res.append(row)
        return Board(res)

    def rotate(self) -> Board:
        return Board(np.rot90(self.matrix))

    def mirror(self) -> Board:
        return Board(np.flip(self.matrix, 1))

    def find_matches(self, snapshot: Board):
        board = self.matrix
        matches = []

        def match_position(pos: [int, int], snapshot: Board):
            for y in range(0, snapshot.size()[1]-1):
                for x in range(0, snapshot.size()[0]-1):
                    cp = add_points(pos, (x, y))
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
                    if match_position((x, y), snapshot):
                        matches.append(((x, y), r))
                    snapshot = snapshot.rotate()

        return matches


def matrix_to_txt(m):
    return '\n'.join([''.join(r) for r in m])


def txt_to_matrix(t):
    return [list(snr) for snr in t.split('\n') if len(snr) > 0]

