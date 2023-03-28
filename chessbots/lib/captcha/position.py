from chessbots.tool.pattern_creator import *
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
    def __init__(self, index, read_style: int, pattern: Board):
        self.usable = False
        self.index = index
        self.pattern = pattern
        self.read_style = read_style
        match self.index:
            case 0:
                self.bit_raw = self.pattern.bits()
                self.check_expect = '00'
            case 1:
                self.bit_raw = self.pattern.fliplr().bits(True)
                self.check_expect = '01'
            case 2:
                self.bit_raw = self.pattern.flipud().bits(True)
                self.check_expect = '10'
            case 3:
                self.bit_raw = self.pattern.flip().bits()
                self.check_expect = '11'
            case _:
                raise RuntimeError('Invalid value section index')

        self.bit_value = self.bit_raw[1:-1]
        self.bit_check = ''.join([self.bit_raw[0], self.bit_raw[-1]])
        self.bit_int = -1
        if "2" not in self.bit_value:
            self.bit_int = bit_to_int(self.bit_value)

    def has_usable_value(self) -> bool:
        if "2" in self.bit_value:
            return False
        if 100 * 100 < bit_to_int(self.bit_value):
            return False
        return True

    def passes_check_bits(self, strict: bool = True) -> bool:
        if self.check_expect == self.bit_check:
            return True
        if strict:
            return False
        if self.bit_check[1] == '2' and self.check_expect[0] == self.bit_check[0]:
            return True
        elif self.bit_check[0] == '2' and self.check_expect[1] == self.bit_check[1]:
            return True
        return False

    def grid_value(self):
        if not self.has_usable_value():
            return Point(-1, -1)

        pos = int_to_pos(bit_to_int(self.bit_value)).mult(2)
        match self.read_style:
            case 0:
                return pos
            case 1:
                match self.index:
                    case 0 | 1:
                        return pos.add(Point(0, -1))
                    case 2 | 3:
                        return pos.add(Point(0, 1))
            case 2:
                match self.index:
                    case 0 | 2:
                        return pos.add(Point(-1, 0))
                    case 1 | 3:
                        return pos.add(Point(1, 0))
            case 3:
                match self.index:
                    case 0:
                        return pos.add(Point(1, 1))
                    case 1:
                        return pos.add(Point(-1, 1))
                    case 2:
                        return pos.add(Point(1, -1))
                    case 3:
                        return pos.add(Point(-1, -1))


class SectionAssertion:
    def __init__(self, from_point: Point, index: int, read_style: int):
        self.from_point = from_point
        self.index = index
        self.read_style = read_style

    def compute_expected_bin(self) -> str:
        pos = self.grid_position()
        to_int = int(pos.y * 100 + pos.x)
        bs = '{0:014b}'
        to_text = bs.format(to_int)
        # if self.index in [1, 2]:
            # to_text = invert_zero_one(to_text)
        return to_text

    def vote(self, given: ValueSection):
        expected = self.compute_expected_bin()
        given_bit = given.bit_value
        if len(expected) != len(given_bit):
            print('Cannot compare different length strings', expected, given_bit)
            raise RuntimeError('Cannot compare different length strings')

        votes = []
        for i in range(0, len(expected)):
            be = expected[i]
            bg = given_bit[i]
            if be == bg:
                votes.append(0)
            elif '2' == bg:
                votes.append(1)
            else:
                votes.append(2)

        vote_confirm_negative = len([v for v in votes if v != 0])
        vote_guess = len([v for v in votes if v == 1])
        vote_against = len([v for v in votes if v == 2])

        return vote_confirm_negative, vote_guess, vote_against, expected, given_bit, self.grid_position().txt


    def grid_position(self):
        pos = self.from_point
        match self.read_style:
            case 0:
                pos = pos
            case 1:
                match self.index:
                    case 0 | 1:
                        pos = pos.add(Point(0, 1))
                    case 2 | 3:
                        pos = pos.add(Point(0, -1))
            case 2:
                match self.index:
                    case 0 | 2:
                        pos = pos.add(Point(1, 0))
                    case 1 | 3:
                        pos = pos.add(Point(-1, 0))
            case 3:
                match self.index:
                    case 0:
                        pos = pos.add(Point(0, 0))
                    case 1:
                        pos = pos.add(Point(-1, 0))
                    case 2:
                        pos = pos.add(Point(0, -1))
                    case 3:
                        pos = pos.add(Point(-1, -1))
        return pos.mult(0.5)


class CheckResult:
    def __init__(self, pattern: Board, snapshot_pos: Point, rotation: int, read_style: int):
        self.usable = False
        self.pattern = pattern
        self.snapshot_pos = snapshot_pos
        self.rotation = rotation
        self.read_style = read_style

        # if '2' in self.pattern.txt():
        #     return
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
            ValueSection(0, self.read_style, self.pattern.create_snapshot(self.pattern_points[0], Point(4, 4))),
            ValueSection(1, self.read_style, self.pattern.create_snapshot(self.pattern_points[1], Point(4, 4))),
            ValueSection(2, self.read_style, self.pattern.create_snapshot(self.pattern_points[2], Point(4, 4))),
            ValueSection(3, self.read_style, self.pattern.create_snapshot(self.pattern_points[3], Point(4, 4))),
        ]
        self.validity_check_check_bits = True if '00011011' == ''.join([s.bit_check for s in self.sections]) else False
        # self.usable = self.validity_check_check_bits
        a: ValueSection
        b: ValueSection
        c: ValueSection
        d: ValueSection
        a, b, c, d = self.sections



        check_results = [s.passes_check_bits(False) for s in self.sections]
        check_results_with_tolerance = [s.passes_check_bits(False) for s in self.sections]
        section_value_checks = [s.has_usable_value() for s in self.sections]
        section_values = [s.grid_value() for s in self.sections]
        section_values_set = set(section_values)
        self.rs_position = Point(-1, -1)
        self.note = ''
        # the lucky case:
        # all resolve totally with positions
        # three resolve totally with positions
        #   not resolving has checkbits positive with tolerance
        if False not in check_results and False not in section_value_checks and 1 == len(section_values_set):
            self.rs_position = section_values_set.pop()
            self.usable = True
        else:
            sections_with_valid_check_bits = [s for s in self.sections if s.passes_check_bits(False)]
            self.usable = True
            if 0 == len(sections_with_valid_check_bits):
                self.note = 'invalid check bits'
                self.usable = False
                # return

            sections_with_position = [s for s in sections_with_valid_check_bits if s.has_usable_value()]

            if 2 > len(sections_with_position):
                self.note = 'not enough usable sections'
                self.usable = False
                # return

            set_pos = [s.grid_value() for s in sections_with_position]
            if 0 == len(set(set_pos)):
                self.note = "empty set pos"
                self.usable = False
                # return
            if 1 != len(set(set_pos)):
                self.note = "Grid values are not equal"
                self.usable = False
                # return
            else:

                sets = [0, 1, 2, 3]
                missing = [i for i in sets if i not in [s.index for s in sections_with_position]]

                missing_sections = [SectionAssertion(set_pos[0], i, read_style) for i in missing]

                msr = [m for m in missing_sections if m.vote(self.sections[m.index])[2] == 0]
                if len(missing_sections) != len(msr):
                    self.note = 'msr', [m.vote(self.sections[m.index]) for m in missing_sections]
                    self.usable = False
                    # return

                self.rs_position = set_pos[0]
                # self.usable = True











        # a, b, c, d = [s.pos_value for s in self.sections]

        # match self.read_style:
        #     case 0:
        #         if a == b == c == d:
        #             self.rs_position = a.mult(2)
        #             self.usable = self.validity_check_check_bits
        #     case 1:
        #         if Point(0, -1) == c.sub(a) and Point(0, -1) == d.sub(b) and a.add(c) == b.add(d):
        #             self.rs_position = a.add(c)
        #             self.usable = self.validity_check_check_bits
        #     case 2:
        #         if Point(-1, 0) == b.sub(a) and Point(-1, 0) == d.sub(c) and a.add(b) == c.add(d):
        #             self.rs_position = a.add(b)
        #             self.usable = self.validity_check_check_bits
        #     case 3:
        #         rp1 = Point(b.x, c.y)
        #         rp2 = Point(c.x, b.y)
        #         if Point(1, 1) == a.sub(d) and Point(-1, -1) == rp1.sub(rp2) and a.add(d) == b.add(c):
        #             self.rs_position = a.add(d)
        #             self.usable = self.validity_check_check_bits

        #
        #
        #
        # rm = self.read_style_mod
        # ppm = self.pattern_point_modifiers
        # self.solved_sections = [
        #     self.sections[0].pos_value.add(ppm[0]).sub(rm),
        #     self.sections[1].pos_value.add(ppm[1]).sub(rm),
        #     self.sections[2].pos_value.add(ppm[2]).sub(rm),
        #     self.sections[3].pos_value.add(ppm[3]).sub(rm),
        # ]
        #
        # self.validity_check_solved_sections_unique = True if 1 == len(set([s.raw for s in self.solved_sections])) else False
        # self.validity_check_check_bits = True if '00011011' == ''.join([s.bit_check for s in self.sections]) else False
        # if not self.validity_check_check_bits:
        #     return
        #
        # if not self.validity_check_solved_sections_unique:
        #     return
        #
        # self.usable = True
        # self.solved_position = self.solved_sections[0]
def get_grid_dimensions(raw: [Point]):
    gminx = min([r.x for r in raw])
    gmaxx = max([r.x for r in raw])
    gminy = min([r.y for r in raw])
    gmaxy = max([r.y for r in raw])

    return gminx, gmaxx, gminy, gmaxy


class GriddedCheckResult:
    def __init__(self, pos: Point, result: CheckResult):
        self.pos = pos
        self.result = result


class Grid:
    def __init__(self, grid: [GriddedCheckResult]):
        self.grid_length = len(grid)
        # if 9 == self.grid_length


def vote_part(sn: Board, raw: Board) -> [int, int, int, [], Board]:
    sn_bit = sn.bits()
    raw_bit = raw.bits()

    if len(sn_bit) != len(raw_bit):
        print('compared unequal bit length')
        return
    votes = []
    for i in range(0, len(sn_bit)):
        expect = sn_bit[i]
        actual = raw_bit[i]
        if expect == actual:
            vote = 0 # match
        elif actual == '2':
            vote = 1 # match against unknown value
        else:
            vote = 2 # mismatch

        votes.append([expect, actual, vote])

    match = len([v for v in votes if v[2] == 0])
    semimatch = len([v for v in votes if v[2] == 1])
    mismatch = len([v for v in votes if v[2] == 2])

    return match, semimatch, mismatch, votes, sn


def vote_grids(snapshot: Board, raw: Board, pos: Point, gcr: GriddedCheckResult):
    raw_board = raw.create_snapshot(pos, snapshot.size())
    votes = []
    for x in range(0, 16, 4):
        for y in range(0, 16, 4):
            sn_part = snapshot.create_snapshot(Point(x, y), Point(4, 4))
            raw_part = raw_board.create_snapshot(Point(x, y), Point(4, 4))
            votes.append(vote_part(sn_part, raw_part))

    valid_votes = [v for v in votes if v[0] > 8 and v[2] < 0]

    return get_grid_dimensions([int_to_pos(bit_to_int(v[4].bits())) for v in votes])





def to_grid(rawraw: [CheckResult]):
    raw = [r for r in rawraw if r.usable]
    if not 0 < len(raw):
        return Point(-1, -1), rawraw

    rots = [r.rotation for r in raw]
    rotation = -1
    if 1 == len(set(rots)):
        rotation = rots[0]

    minx, maxx, miny, maxy = get_grid_dimensions([r.rs_position for r in raw])
    return Point(int((minx + maxx) / 2), int((miny + maxy) / 2)), rotation

    # print('tg', gminx, gmaxx, gminy, gmaxy, [r.rs_position.txt for r in raw])

    # ref = raw[0]
    # rest = raw
    # grid = []
    # for x in range(gminx, gmaxx+1):
    #     for y in range(gminy, gmaxy+1):
    #         p = Point(x, y)
    #         filtered_to_pos = [r for r in rest if r.rs_position == p]
    #         # print([f.rs_position.txt for f in filtered_to_pos], [f.rs_position.txt for f in rest])
    #         if 1 == len(filtered_to_pos):
    #             found: CheckResult = filtered_to_pos[0]
    #             from_center_mod = ref.rs_position.sub(p)
    #             expected_snapshot_position = ref.snapshot_pos.sub(from_center_mod.mult(4))
    #             # print('expecz', p.txt, ref.rs_position.txt, ref.snapshot_pos.txt, from_center_mod.txt, expected_snapshot_position.txt, found.snapshot_pos.txt)
    #             if found.snapshot_pos == expected_snapshot_position:
    #                 rest = [r for r in rest if r.rs_position != p]
    #                 grid.append(GriddedCheckResult(Point(x - gminx, y - gminy), found))
    #
    # # print('rest', rest, 'grid', grid)
    #
    # minx, maxx, miny, maxy = get_grid_dimensions([r.rs_position for r in raw])
    # grid_length = len(grid)
    # if 9 == grid_length:
    #     return Point(int((minx + maxx)/2), int((miny + maxy)/2)), grid
    # elif 1 == grid_length:
    #     # construct surrounding field
    #     pos = grid[0].result.rs_position
    #     read_style = grid[0].result.read_style
    #     board = Pattern8x8With4DataFields().create(800)
    #     sn_pos = pos.sub(Point(1, 1)).mult(4)
    #     sn_size = Point(16, 16)
    #
    #     snapshot = board.create_snapshot(sn_pos, sn_size)
    #
    #     minx, maxx, miny, maxy = vote_grids(snapshot, raw_board, grid[0].result.snapshot_pos.sub(Point(4, 4)), grid[0])
    #
    #     # compare raw grid with construct
    #     # based on matches assume missing grid fields
    #
    #
    # p = Point(int((minx + maxx)/2), int((miny + maxy)/2))
    #
    # return p, grid


def check_results_to_one(results: [CheckResult]) -> [Point, []]:
    # has center result
    results = [r for r in results if r.usable]
    foo = [r for r in results if r.has_center_point]
    # print(foo)
    if 1 == len(foo):
        center_result: CheckResult = foo[0]
        gminx = min([r.rs_position.x for r in results])
        gmaxx = max([r.rs_position.x for r in results])
        gminy = min([r.rs_position.y for r in results])
        gmaxy = max([r.rs_position.y for r in results])
        grid = [center_result]
        for x in range(gminx, gmaxx):
            for y in range(gminy, gmaxy):
                p = Point(x, y)
                filtered_to_pos = [r for r in results if r.rs_position == p]
                # print([f.rs_position for f in filtered_to_pos])
                if 1 == len(filtered_to_pos):
                    found: CheckResult = filtered_to_pos[0]
                    from_center_mod = center_result.rs_position.sub(p)
                    expected_snapshot_position = center_result.snapshot_pos.sub(from_center_mod.mult(4))
                    if found.snapshot_pos == expected_snapshot_position:
                        grid.append(found)

        return Point(-2, -2), grid
    return Point(-1, -1), []


def resolve_board_to_position(board: Board):
    snapshot_size = Point(8, 8)
    results = []
    for rotate_step in range(0, 4):
        for x in range(0, board.size().x - snapshot_size.x + 1):
            for y in range(0, board.size().y - snapshot_size.y + 1):
                for read_style in [0, 1, 2, 3]:
                    pos = Point(x, y)
                    results.append(CheckResult(
                        board.create_snapshot(Point(x, y), snapshot_size),
                        pos,
                        rotate_step,
                        read_style
                    ))
        board = board.rotate()

    # to_one = check_results_to_one(results)
    filtered = [r for r in results if r.usable]
    to_one, rotation = to_grid(filtered)

    return to_one, rotation, results

