from chessbots.lib.pattern import Pattern as Board
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
        b.create_snapshot(Point(0, 0), Point(4, 4)).bits(),
        b.create_snapshot(Point(4, 0), Point(4, 4)).fliplr().bits(True),
        b.create_snapshot(Point(4, 4), Point(4, 4)).flip().bits(),
        b.create_snapshot(Point(0, 4), Point(4, 4)).flipud().bits(True),
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
    return Point(val % size, val // size)


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
    raw_bits = get_section_bits(section)
    bits = [b[1:-1] for b in raw_bits]
    check_bits = ''.join([''.join([b[0], b[-1]]) for b in raw_bits])
    # print(check_bits)
    # print('error', section.txt(), bits)
    result = calc_votes(bits)

    bins = [r[0] for r in result]
    if 2 in bins:
        return

    if '00101101' != check_bits:
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
        # print('length error', lens, lenset, bits)
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


def get_section_bits_for_pattern(b: Board, pattern: int):
    match pattern:
        case 0:
            pattern_points = [
                Point(0, 0),
                Point(4, 0),
                Point(0, 4),
                Point(4, 4),
            ]
        case 1:
            pattern_points = [
                Point(0, 4),
                Point(4, 4),
                Point(0, 0),
                Point(4, 0),
            ]
        case 2:
            pattern_points = [
                Point(4, 0),
                Point(0, 0),
                Point(4, 4),
                Point(0, 4),
            ]
        case 3:
            pattern_points = [
                Point(4, 4),
                Point(0, 4),
                Point(4, 0),
                Point(0, 0),
            ]
        case _:
            raise RuntimeError('Bad pattern index: ' + str(pattern))

    return [
            b.create_snapshot(pattern_points[0], Point(4, 4)).bits(),
            b.create_snapshot(pattern_points[1], Point(4, 4)).fliplr().bits(True),
            b.create_snapshot(pattern_points[2], Point(4, 4)).flipud().bits(True),
            b.create_snapshot(pattern_points[3], Point(4, 4)).flip().bits(),
        ]


class ValueSection:
    def __init__(self, index, pattern: Board):
        self.index = index
        self.pattern = pattern
        match self.index:
            case 0:
                self.bit_raw = self.pattern.bits()
                self.check_expect = '00'
            case 1:
                self.bit_raw = self.pattern.fliplr().bits(True)
                self.check_expect = '10'
            case 2:
                self.bit_raw = self.pattern.flipud().bits(True)
                self.check_expect = '01'
            case 3:
                self.bit_raw = self.pattern.flip().bits()
                self.check_expect = '11'
            case _:
                raise RuntimeError('Invalid value section index')

        self.bit_value = self.bit_raw[1:-1]
        self.bit_check = ''.join([self.bit_raw[0], self.bit_raw[-1]])

        self.int_value = bit_to_int(self.bit_value)
        self.pos_value = int_to_pos(self.int_value)



class CheckResult:
    def __init__(self, pattern: Board, snapshot_pos: Point, rotation: int, read_style: int):
        self.usable = False
        self.pattern = pattern
        self.snapshot_pos = snapshot_pos
        self.rotation = rotation
        self.read_style = read_style

        if '2' in self.pattern.txt():
            return
        '''
            1x1 1x1   2x1 2x1   3x1 3x1  
            1x1 1x1   2x1 2x1   3x1 3x1
        
            1x2 1x2   2x2 2x2   3x2 3x2
            1x2 1x2   2x2 2x2   3x2 3x2
        
            1x3 1x3   2x3 2x3   3x3 3x3
            1x3 1x3   2x3 2x3   3x3 3x3
        
        -
            1x1   1x1 2x1   2x1 3x1   3x1
              
            1x1   1x1 2x1   2x1 3x1   3x1
            1x2   1x2 2x2   2x2 3x2   3x2
            
            1x2   1x2 2x2   2x2 3x2   3x2
            1x3   1x3 2x3   2x3 3x3   3x3
            
            1x3   1x3 2x3   2x3 3x3   3x3
        -
        
        0x0  0.5x0.5
            0x0 0x0  
            0x0 0x0
        0x1  0.5x1:
            0x0 0x0  
            0x1 0x1
        1x0  1x0.5:
            0x0 1x0  
            0x0 1x0
        1x1  4x4
            0x0 1x0
            0x1 1x1
        2x2 8x8
            1x1 1x1
            1x1 1x1
        3x3 12x12
            1x1 2x1
            1x2 2x2
        4x4 16x16
            2x2 2x2
            2x2 2x2    
        
        
        
        
        
            # 0 - 1x1 1x1 1x1 1x1 
        '''
        match self.read_style:
            case 0:
                # 01 1x1 1x1
                # 23 1x1 1x1
                self.pattern_points = [Point(0, 0), Point(4, 0), Point(0, 4), Point(4, 4)]
                self.pattern_point_modifiers = [Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)]
                self.read_style_mod = Point(0.5, 0.5)
            case 1:
                # 23 1x2 1x2
                # 01 1x1 1x1
                self.pattern_points = [Point(0, 4), Point(4, 4), Point(0, 0), Point(4, 0)]
                self.pattern_point_modifiers = [Point(0.5, 0), Point(0.5, 0), Point(0.5, 1), Point(0.5, 1)]
                self.read_style_mod = Point(0, 1)
            case 2:
                # 10 2x1 1x1
                # 32 2x1 1x1
                self.pattern_points = [Point(4, 0), Point(0, 0), Point(4, 4), Point(0, 4)]
                self.pattern_point_modifiers = [Point(0, 0.5), Point(-1, 0.5), Point(0, 0.5), Point(-1, 0.5)]
                self.read_style_mod = Point(1, 0)
            case 3:
                # 32  2x2 2x1
                # 10  1x2 1x1
                self.pattern_points = [Point(4, 4), Point(0, 4), Point(4, 0), Point(0, 0)]
                self.pattern_point_modifiers = [Point(1, 1), Point(0, 1), Point(1, 0), Point(0, 0)]
                self.read_style_mod = Point(1, 1)
            case _:
                raise RuntimeError('Bad read style: ' + str(self.read_style))

        self.sections = [
            ValueSection(0, self.pattern.create_snapshot(self.pattern_points[0], Point(4, 4))),
            ValueSection(1, self.pattern.create_snapshot(self.pattern_points[1], Point(4, 4))),
            ValueSection(2, self.pattern.create_snapshot(self.pattern_points[2], Point(4, 4))),
            ValueSection(3, self.pattern.create_snapshot(self.pattern_points[3], Point(4, 4))),
        ]

        rm = self.read_style_mod
        ppm = self.pattern_point_modifiers
        self.solved_sections = [
            self.sections[0].pos_value.add(ppm[0]).sub(rm),
            self.sections[1].pos_value.add(ppm[1]).sub(rm),
            self.sections[2].pos_value.add(ppm[2]).sub(rm),
            self.sections[3].pos_value.add(ppm[3]).sub(rm),
        ]

        self.validity_check_solved_sections_unique = True if 1 == len(set([s.raw for s in self.solved_sections])) else False
        self.validity_check_check_bits = True if '00011011' == ''.join([s.bit_check for s in self.sections]) else False
        if not self.validity_check_check_bits:
            return

        if not self.validity_check_solved_sections_unique:
            return

        self.usable = True
        self.solved_position = self.solved_sections[0]


class CheckResultCollection:
    def __init__(self, results: [CheckResult]):
        self.results = results


def resolve_board_to_position(board: Board):
    snapshot_size = Point(8, 8)
    results = []
    for rotate_step in range(0, 4):
        for x in range(0, board.size().x - snapshot_size.x + 1):
            for y in range(0, board.size().y - snapshot_size.y + 1):
                for read_style in [0, 1, 2, 3]:
                    results.append(CheckResult(
                        board.create_snapshot(Point(x, y), snapshot_size),
                        Point(x, y),
                        rotate_step,
                        read_style
                    ))
        board = board.rotate()

    filtered = [r for r in results if r.usable]
    collection = CheckResultCollection(filtered)
    print(filtered)
    has_unique_result = True if 1 == len(set([s.solved_position.raw for s in filtered])) else False
    if has_unique_result:
        return filtered[0].solved_position, results

    return Point(-1, -1), results

