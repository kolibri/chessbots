from chessbots.lib.pattern import Pattern as Board
from chessbots.lib.pattern import txt_to_matrix
from chessbots.lib.point_helper import *
from typing import NamedTuple


class MatchResult(NamedTuple):
    bits: [str]
    matching: int
    value: int
    snapshot: Board
    position: Point


def get_section_bits(b: Board):
    return [
        b.create_snapshot(Point(0, 0), Point(4, 4)).bits(True),
        b.create_snapshot(Point(4, 0), Point(4, 4)).fliplr().bits(),
        b.create_snapshot(Point(4, 4), Point(4, 4)).flip().bits(True),
        b.create_snapshot(Point(0, 4), Point(4, 4)).flipud().bits(),
    ]


def get_mismatches(seq1: str, seq2: str):
    def get_mod(a: int, b: int):
        if 2 == a or 2 == b:
            return 3

        return 1 if a != b else 0

    count = sum(get_mod(int(a), int(b)) for a, b in zip(seq1, seq2))
    return count


def bit_to_int(bit: str) -> int:
    return int(bit, 2)


def int_to_pos(val: int) -> Point:
    size = 100
    return Point(val // size, val % size)


def calc_matching(bits: [str]):
    return sum([
        get_mismatches(bits[0], bits[1]),
        get_mismatches(bits[0], bits[2]),
        get_mismatches(bits[0], bits[3]),
        get_mismatches(bits[1], bits[2]),
        get_mismatches(bits[1], bits[3]),
        get_mismatches(bits[2], bits[3]),
    ])


def create_solution(section: Board, at_pos: Point, rot: int):
    bits = get_section_bits(section)
    result = calc_votes(bits)

    bins = [r[0] for r in result]
    if 2 in bins:
        return

    binstring = ''.join([str(b) for b in bins])
    intval = bit_to_int(binstring)
    if not intval < 10000:
        return

    votes = calc_votes(bits)
    vote_result = calc_vote_result(votes)
    guess = Guess(vote_result[0], at_pos)
    return Solution(
        section,
        at_pos,
        rot,
        bits,
        votes,
        vote_result,
        guess
    )


def calc_votes(bits: [str]):
    def vote_value(bits: [str, str, str, str], i: int):
        # -> [value, positive_votes, negative_votes, no_vote, raw]

        letters = [bits[0][i], bits[1][i], bits[2][i], bits[3][i]]
        letters = [int(i) for i in letters]
        a, b, c, d = letters
        # if a == b == c == d:
        #     return [a, 4, 0, 0, letters]

        zero_count = sum([1 for m in letters if m == 0])
        ones_count = sum([1 for m in letters if m == 1])
        twos_count = sum([1 for m in letters if m == 2])

        if ones_count == 0 and zero_count > 0:
            return [0, 4 - zero_count, ones_count, twos_count, letters]
        if zero_count == 0 and ones_count > 0:
            return [1, 4 - ones_count, zero_count, twos_count, letters]
        if twos_count <= 1 and zero_count > ones_count:
            return [0, 4 - zero_count, ones_count, twos_count, letters]
        if twos_count <= 1 and zero_count < ones_count:
            return [1, ones_count, zero_count, twos_count, letters]
        return [2, 4, 4 - zero_count + ones_count, twos_count, letters]

    lens = [len(b) for b in bits]
    lenset = set(lens)
    if 1 != len(lenset):
        raise RuntimeError('matching only works with all equal length strings')
    size = len(bits[0])

    result = []
    for i in range(0, size):
        r = vote_value(bits, i)
        # print('r', r)
        result.append(r)
    return result


def calc_vote_result(votes: []):
    return [
        ''.join([str(v[0]) for v in votes]),
        sum([v[1] for v in votes]),
        sum([v[2] for v in votes]),
        sum([v[3] for v in votes]),
    ]


class Guess:
    def __init__(self, bins: str, at: Point):
        self.bins = bins
        self.bint = bit_to_int(self.bins)
        self.pos = int_to_pos(self.bint)
        self.mult_pos = mult_point(self.pos, 8)
        self.solved = sub_points(self.mult_pos, at)

    def value(self):
        return self.pos, self.bint, self.bins, self.mult_pos


class Solution(NamedTuple):
    section: Board
    pos: Point
    rotation: int
    bits: [str, str, str, str]
    votes: [[int, int, int, int, [int, int, int, int]]]
    vote_result: [int, int, int]
    guess: Guess

    # match: any

    def solve(self) -> [Point]:
        return sub_points(self.guess.mult_pos, self.pos)


class CaptchaResolver:
    def resolve(self, board_txt: str):
        board = Board(txt_to_matrix(board_txt))

        size_x, size_y = board.size()
        raw = []
        for rotate_step in range(0, 2):
            for x in range(0, size_x - 7):
                for y in range(0, size_y - 7):
                    section = board.create_snapshot(Point(x, y), Point(8, 8))
                    match = create_solution(section, Point(y, x), rotate_step)
                    if match:
                        # print('solution', match)
                        raw.append(match)
            board = board.rotate()

        # lowest = min([m.votes[0] for m in raw])
        # filtered = [m for m in raw if m.votes[0] == lowest]
        # print(results)
        return raw, raw
