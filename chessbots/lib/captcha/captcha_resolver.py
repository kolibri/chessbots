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


def get_section_bits(bits: [str]):
    return [b[1:-1] for b in bits]


def get_check_bits(bits: [str]):
    return [''.join([b[0], b[15]]) for b in bits]


def get_raw_bits(b: Board):
    return [
        b.create_snapshot(Point(0, 0), Point(4, 4)).bits(True),
        b.create_snapshot(Point(0, 4), Point(4, 4)).flipud().bits(),
        b.create_snapshot(Point(4, 0), Point(4, 4)).fliplr().bits(),
        b.create_snapshot(Point(4, 4), Point(4, 4)).flip().bits(True),
    ]


def get_raw_bits_pos_1(b: Board):
    return [
        b.create_snapshot(Point(0, 0), Point(4, 4)).flip().bits(True),
        b.create_snapshot(Point(0, 4), Point(4, 4)).fliplr().bits(),
        b.create_snapshot(Point(4, 0), Point(4, 4)).flipud().bits(),
        b.create_snapshot(Point(4, 4), Point(4, 4)).bits(True),
    ]


def get_raw_bits_pos_2(b: Board):
    return [
        b.create_snapshot(Point(0, 0), Point(4, 4)).flipud().bits(),
        b.create_snapshot(Point(0, 4), Point(4, 4)).bits(True),
        b.create_snapshot(Point(4, 0), Point(4, 4)).flip().bits(True),
        b.create_snapshot(Point(4, 4), Point(4, 4)).fliplr().bits(),
    ]


def get_raw_bits_pos_3(b: Board):
    return [
        b.create_snapshot(Point(0, 0), Point(4, 4)).fliplr().bits(),
        b.create_snapshot(Point(0, 4), Point(4, 4)).flip().bits(True),
        b.create_snapshot(Point(4, 0), Point(4, 4)).bits(True),
        b.create_snapshot(Point(4, 4), Point(4, 4)).flipud().bits(),
    ]


def get_mismatches(seq1: str, seq2: str):
    def get_mod(a: int, b: int):
        if 2 == a or 2 == b:
            return 3

        return 1 if a != b else 0

    count = sum(get_mod(int(a), int(b)) for a, b in zip(seq1, seq2))
    return count


def bit_to_int(bit: str) -> int:
    if '2' in bit:
        return -1
    return int(bit, 2)


def int_to_pos(val: int) -> Point:
    size = 100
    return Point(val % size, val // size)


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


def validate_check_bits(bits: [str]):
    return '00101101' == ''.join(bits)


class Guess:
    def __init__(self, bins: str, at_pos: Point):
        self.bins = bins
        self.bint = bit_to_int(self.bins)
        self.pos = int_to_pos(self.bint)
        self.solved = add_points(mult_point(self.pos, 8), at_pos)

    def values(self):
        return self.solved, self.bint, self.pos, self.bins


# def get_section_bits(bits: [str]):
#     return [b[1:-1] for b in bits]


# def get_check_bits(bits: [str]):
#     return [''.join([b[0], b[15]]) for b in bits]
class ValueField:
    def __init__(self, bitstring):
        self.bitstring = bitstring
        self.value = self.bitstring[1:-1]
        self.check = ''.join([self.bitstring[0], self.bitstring[len(self.bitstring) - 1]])
        self.value_int = bit_to_int(self.value)
        self.value_pos = int_to_pos(self.value_int)


class PatternSolution:
    def __init__(self, id: str, bits: [str, str, str, str], at_pos: Point):
        self.id = id
        self.at_pos = at_pos

        self.bits = [ValueField(f) for f in bits]
        self.solved_bits = self.solve_bits()
        self.value_bits = [f.value for f in self.bits]
        self.value_ints = [f.value_int for f in self.bits]
        self.value_poss = [f.value_pos for f in self.bits]
        self.check_bits = [f.check for f in self.bits]
        self.check_bits_result = validate_check_bits(self.check_bits)

        self.votes = calc_votes(self.value_bits)
        self.vote_result = calc_vote_result(self.votes)
        self.guess = Guess(self.vote_result[0], self.at_pos)

    def solve_to_one(self):
        r = list(set(self.solve_bits()))
        if 1 != len(r):
            return False

        return r[0]

    def solve_bits(self):
        if '00' == self.id:
            return [sub_points(mult_point(b.value_pos, 8), self.at_pos) for b in self.bits]
        if '01' == self.id:
            return [
                sub_points(mult_point(self.bits[0].value_pos, 8), add_points(Point(-4, 0), self.at_pos)),
                sub_points(mult_point(self.bits[1].value_pos, 8), add_points(Point(-4, 0), self.at_pos)),
                sub_points(mult_point(self.bits[2].value_pos, 8), add_points(Point(4, 0), self.at_pos)),
                sub_points(mult_point(self.bits[3].value_pos, 8), add_points(Point(4, 0), self.at_pos)),
            ]
        if '10' == self.id:
            return [
                sub_points(mult_point(self.bits[0].value_pos, 8), add_points(Point(0, -4), self.at_pos)),
                sub_points(mult_point(self.bits[1].value_pos, 8), add_points(Point(0, 4), self.at_pos)),
                sub_points(mult_point(self.bits[2].value_pos, 8), add_points(Point(0, -4), self.at_pos)),
                sub_points(mult_point(self.bits[3].value_pos, 8), add_points(Point(0, 4), self.at_pos)),
            ]
        if '11' == self.id:
            return [
                sub_points(mult_point(self.bits[0].value_pos, 8), add_points(Point(-4, -4), self.at_pos)),
                sub_points(mult_point(self.bits[1].value_pos, 8), Point(self.at_pos.x - 4, self.at_pos.y + 4)),
                sub_points(mult_point(self.bits[2].value_pos, 8), Point(self.at_pos.x + 4, self.at_pos.y - 4)),
                sub_points(mult_point(self.bits[3].value_pos, 8), add_points(Point(4, 4), self.at_pos)),
            ]


class Solution:
    section: Board
    pos: Point
    rotation: int
    pattern: []

    def __init__(self, section: Board, pos: Point, rot: int):
        self.section = section
        self.pos = pos
        self.rotation = rot

        self.pattern = []
        # self.pattern = [
        #     PatternSolution('00', get_raw_bits(section), self.pos),
        #     PatternSolution('01', get_raw_bits_pos_3(section), self.pos),
        #     PatternSolution('10', get_raw_bits_pos_2(section), self.pos),
        #     PatternSolution('11', get_raw_bits_pos_1(section), self.pos),
        # ]

    def validate(self) -> bool:
        if 0 == len([p for p in self.pattern if p.solve_to_one()]):
            return False
        # if not self.validate_check_bits():
        #     return False
        # if not self.guess.bint < 10000:
        #     return False
        return True

    def solve(self) -> [Point]:
        p = [p.solve_to_one() for p in self.pattern if p.solve_to_one()]
        p = list(set(p))

        if 1 != len(p):
            return
        return p[0]


def choose_solution(solutions: [Solution]):

    rots = list(set([sol.rotation for sol in solutions]))
    rots = [[r, [s for s in solutions if s.rotation == r]] for r in rots]
    rots = [[r[0], len(r[1]), [s.solve() for s in r[1]], r[1]] for r in rots]
    max_rots = [r[1] for r in rots]
    if not 0 < len(max_rots):
        print('no solutions left for max', solutions)
        return
    rots = [r for r in rots if r[1] == max(max_rots)]

    sol = list(set(rots[0][2]))
    sol = sol[0]
    return sol, rots[0][0], rots[0][1] #, rots
    # def filter_solutions(filter):
    #     return [s for s in solutions if s.solve() == filter]
    #
    # # print('cs', solutions)
    # if solutions == []:
    #     return 'No solution',
    # vals = [s.solve() for s in solutions]
    # vals = list(set(vals))
    # # print(vals)
    # count = [[v, len(filter_solutions(v)), filter_solutions(v)] for v in vals]
    # max_count = max([c[1] for c in count])
    # max_values = [c for c in count if c[1] == max_count]
    # print('ch', max_count, len(max_values), max_values)
    # if 1 == len(max_values):
    #     return max_values[0]
    # print('')
    # return 'to many',


class CaptchaResolver:
    def resolve(self, board_txt: str):
        board = Board(txt_to_matrix(board_txt))

        size_x, size_y = board.size()
        raw = []
        for rotate_step in [0, 90, 180, 270]:
            for x in range(0, size_x - 7):
                for y in range(0, size_y - 7):
                    section = board.create_snapshot(Point(x, y), Point(8, 8))
                    raw.append(Solution(section, Point(x, y), rotate_step))
            board = board.rotate()

        # lowest = min([m.votes[0] for m in raw])
        # filtered = [m for m in raw if m.votes[0] == lowest]
        # print(results)
        filtered = [r for r in raw if r.validate()]
        choose = choose_solution(filtered)
        print('choose', choose)
        return filtered, choose, raw
