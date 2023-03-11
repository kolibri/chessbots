import numpy as np
from textwrap import wrap
from chessbots.lib.pattern import *


class PatternCreator:
    def create(self, size: int):
        pass


class Pattern8x8With4DataFields(PatternCreator):
    def create_captcha(self, index: int):
        bs = '{0:016b}'
        bits = bs.format(index)
        bits_inverted = bits.replace('0', 'n').replace('1', '0').replace('n', '1')

        bits_matrix = Pattern(txt_to_matrix('\n'.join(wrap(bits, 4)))).matrix
        bits_inverted_matrix = Pattern(txt_to_matrix('\n'.join(wrap(bits_inverted, 4)))).matrix

        return Pattern(self.combine(
            [
                [bits_matrix, np.fliplr(bits_inverted_matrix)],
                [np.flipud(bits_inverted_matrix), np.flip(bits_matrix)]
            ]
        ))

    def create(self, size: int) -> Pattern:
        pattern_size = 8
        if 0 != size % pattern_size:
            print('Warning: field size not divisible py pattern size')

        pattern_per_side = int(size / pattern_size)
        pr = range(0, pattern_per_side)

        captchas = [[self.create_captcha(r+c*pattern_per_side).matrix for r in pr] for c in pr]

        return Pattern(self.combine(captchas))

    def combine(self, patterns):
        return np.concatenate([np.concatenate(rows, axis=1) for rows in patterns], axis=0)
