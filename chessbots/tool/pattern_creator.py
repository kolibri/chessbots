import numpy as np
from textwrap import wrap
from chessbots.lib.pattern import *


class PatternCreator:
    def create(self, size: int):
        pass


def bits_to_pattern(bits: str) -> Pattern:
    return Pattern(txt_to_matrix('\n'.join(wrap(bits, 4))))


class Pattern8x8With4DataFields(PatternCreator):
    def create(self, size: int) -> Pattern:
        pattern_size = 8
        if 0 != size % pattern_size:
            print('Warning: field size not divisible py pattern size')

        pattern_per_side = int(size / pattern_size)
        pr = range(0, pattern_per_side)

        captchas = [[self._create_captcha(r + c * pattern_per_side).matrix for r in pr] for c in pr]

        return Pattern(self._combine(captchas))

    def _create_captcha(self, index: int):
        bs = '{0:014b}'
        bits = bs.format(index)
        bits_inverted = invert_zero_one(bits)

        fields = [
            [
                bits_to_pattern('0' + bits + '0').matrix,
                bits_to_pattern('1' + bits_inverted + '0').fliplr().matrix,
            ], [
                bits_to_pattern('0' + bits_inverted + '1').flipud().matrix,
                bits_to_pattern('1' + bits + '1').flip().matrix,
            ]
        ]

        return Pattern(self._combine(fields))

    @staticmethod
    def _combine(patterns):
        return np.concatenate([np.concatenate(rows, axis=1) for rows in patterns], axis=0)
