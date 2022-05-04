def create_chunks(number):
    width = 4
    length = width * width

    bin_string = bin(number)[2:].zfill(length)
    chunks = [bin_string[i:i + width] for i in range(0, len(bin_string), width)]
    return chunks


def create_row_from_chunks(row, index):
    line = [chunk[index] for chunk in row]
    return ''.join(line)


def create_snapshot(board, position, size):
    board = board.split('\n')
    x1 = position[0]
    x2 = position[0] + size[0]
    y1 = position[1]
    y2 = position[1] + size[1]
    cols = []
    for c in range(y1, y2):
        line = ''.join(board[c])
        part = line[x1:x2]
        cols.append(part)

    foo = '\n'.join(cols)
    return foo


def rotate(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def create_txt_board(field_width):
    rows = []
    for y in range(0, field_width):
        row_chunks = [create_chunks(c) for c in range(y * field_width, y * field_width + field_width)]
        chunked_rows = [create_row_from_chunks(row_chunks, i) for i in range(0, 4)]
        for chunked_row in chunked_rows:
            rows.append(chunked_row)
    return '\n'.join(rows)


def create_snapshot_rotations(r0):
    r1 = rotate(r0)
    r2 = rotate(r1)
    r3 = rotate(r2)
    return r0, r1, r2, r3


def matrix_to_txt(m):
    return '\n'.join([''.join(r) for r in m])


def txt_to_matrix(t):
    return [list(snr) for snr in t.split('\n')]


def find_matches(board, snapshot):
    matches = []
    sn_size = (8, 8)

    for y in range(0, len(board) - sn_size[1] - 1):
        for x in range(0, len(board[y]) - sn_size[0] - 1):
            current = txt_to_matrix(create_snapshot(matrix_to_txt(board), (x, y), sn_size))
            if current == snapshot:
                matches.append((x, y))
                # print('MATCH')

    return matches


tb = create_txt_board(100)
f = open("txtboard.txt", "w")
f.write(tb)
f.close()

tbm = txt_to_matrix(tb)
snm = txt_to_matrix(create_snapshot(tb, (0, 0), (8, 8)))

print(matrix_to_txt(tbm))
print('----------')
print(matrix_to_txt(snm))
print('----------')
#
# rots = create_snapshot_rotations(snm)
# print(matrix_to_txt(tbm), matrix_to_txt(snm))
print('Find matches:')
m = find_matches(tbm, snm)
mr1 = rotate(snm)
mr2 = rotate(mr1)
mr3 = rotate(mr2)
m1 = find_matches(tbm, mr1)
m2 = find_matches(tbm, mr2)
m3 = find_matches(tbm, mr3)


print('Summary matches:', m, m1, m2, m3)