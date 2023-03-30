from chessbots.lib.pattern import Pattern as Board
from chessbots.lib.point_helper import *


def bit_to_int(bit: str) -> int:
    return int(bit, 2)


def int_to_pos(val: int) -> Point:
    size = 100
    return Point(val % size, val // size)


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
            case 0: # 0
                self.pattern_points = [Point(0, 0), Point(4, 0), Point(0, 4), Point(4, 4)]
            case 1: # >
                self.pattern_points = [Point(0, 4), Point(4, 4), Point(0, 0), Point(4, 0)]
            case 2: # v
                self.pattern_points = [Point(4, 0), Point(0, 0), Point(4, 4), Point(0, 4)]
            case 3: # +
                self.pattern_points = [Point(4, 4), Point(0, 4), Point(4, 0), Point(0, 0)]
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
        section_value_checks = [s.has_usable_value() for s in self.sections]
        section_values = [s.grid_value() for s in self.sections]
        section_values_set = set(section_values)
        self.rs_position = Point(-1, -1)
        self.note = ''

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


def get_grid_dimensions(raw: [Point]):
    gminx = min([r.x for r in raw])
    gmaxx = max([r.x for r in raw])
    gminy = min([r.y for r in raw])
    gmaxy = max([r.y for r in raw])

    return gminx, gmaxx, gminy, gmaxy


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

    filtered = [r for r in results if r.usable]
    to_one, rotation = to_grid(filtered)

    return to_one, rotation, results

