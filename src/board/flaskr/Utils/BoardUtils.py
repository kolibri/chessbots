import time
from ..BotData.Board import *
from ..BotData.PointHelper import *


def create_txt_board_4x4_bin(field_width):
    def create_chunks(number):
        width = 4
        length = width * width

        bin_string = bin(number)[2:].zfill(length)
        chunks = [bin_string[i:i + width] for i in range(0, len(bin_string), width)]
        return chunks

    def create_row_from_chunks(row, index):
        line = [chunk[index] for chunk in row]
        return ''.join(line)

    rows = []
    for y in range(0, field_width):
        row_chunks = [create_chunks(c) for c in range(y * field_width, y * field_width + field_width)]
        chunked_rows = [create_row_from_chunks(row_chunks, i) for i in range(0, 4)]
        for chunked_row in chunked_rows:
            rows.append(chunked_row)
    return '\n'.join(rows)


def create_txt_board_empty(size):
    return '\n'.join(['0' * size for y in range(0, size)])


def create_txt_board_full(size):
    return '\n'.join(['1' * size for y in range(0, size)])


class BoardChecker:
    def __init__(self, board: Board, snapshot_size: (int, int)):
        self.board = board
        self.snapshot_size = snapshot_size
        self.checked = []
        self.cache = {}
        self.batch_size = 10

    def check_performance(self) -> [str, float, float]:
        results = []
        walk_range = sub_points(self.board.size(), self.snapshot_size)

        current_start = time.time()
        for y in range(0, walk_range[1]):
            for x in range(0, walk_range[0]):
                print('.', end='')
                snapshot = self.board.create_snapshot((x, y), self.snapshot_size)
                self.board.find_matches(snapshot)
        print('')
        current_end = time.time()
        results.append(['current', current_start, current_end])

        return results

    def check_validity(self) -> [[Board], [Board]]:
        results = []
        snapshots = []
        walk_range = sub_points(self.board.size(), self.snapshot_size)

        print('Testing ' + str(walk_range[0] * walk_range[1]) + ' snapshot positions')
        for y in range(0, walk_range[1]):
            for x in range(0, walk_range[0]):
                #print('.' + str(x + y * walk_range[0]), end='')
                snapshot = self.board.create_snapshot((x, y), self.snapshot_size)
                for r in (90, 180, 270, 0):
                    snapshot = snapshot.rotate()
                    if snapshot.txt() not in snapshots:
                        snapshots.append(snapshot.txt())
                    else:
                        results.append(snapshot.txt())
        print('')

        return results, snapshots
