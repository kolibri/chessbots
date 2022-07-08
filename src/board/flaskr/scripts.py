import os
import shutil
from flask import Blueprint
from flask import current_app
from .Utils.BoardUtils import *
from .Utils.BoardImageCreator import *

bp = Blueprint('script', __name__)


def clean_directory(folder: str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# @click.argument('name')
@bp.cli.command('checkboard')
def checkboard():
    board = Board(txt_to_matrix(create_txt_board_4x4_bin(5)))
    snapshot_size = (8, 8)
    checker = BoardChecker(board, snapshot_size)
    print('Start board check')
    print('board size: ' + str(board.size()[0]) + 'x' + str(board.size()[1]))
    print('snapshot size: ' + str(snapshot_size[0]) + 'x' + str(snapshot_size[1]))
    start = time.time()
    results = checker.check_validity()
    end = time.time()

    print(board.txt())
    # for r in results[0]:
    #     print(r)
    #     print('-----')
    # print('')
    # for r in results[1]:
    #     print(r.txt())
    #     print('-----')
    print('Found snapshots: ' + str(len(results[1])))
    print('Found results: ' + str(len(results[0])))
    if not 0 < len(results[0]):
        print('Yay!!')
    print('Duration: ' + str(end - start))
    print('Finished')


@bp.cli.command('performance')
def performance():
    board = Board(txt_to_matrix(create_txt_board_4x4_bin(5)))
    snapshot_size = (8, 8)
    checker = BoardChecker(board, snapshot_size)
    print('Start performance check with ')
    print('board size: ' + str(board.size()[0]) + 'x' + str(board.size()[1]))
    print('snapshot size: ' + str(snapshot_size[0]) + 'x' + str(snapshot_size[1]))

    results = checker.check_performance()
    for r in results:
        print(r[0], str(r[1]), str(r[2]), str(r[2] - r[1]))


@bp.cli.command('cleanup')
def cleanup():
    clean_directory(current_app.config['BOTCACHE_DIR'])


@bp.cli.command('boardprint')
def boardprint():
    base_path = current_app.config['STATIC_DIR']
    pc = BoardImageCreator(int((2000 / 25.4) * 300), 100)
    pc.save_img(base_path + 'prints/print_board.jpeg')


@bp.cli.command('mockimages')
def mockimages():
    base_path = current_app.config['STATIC_DIR']
    pc = BoardImageCreator(2000, 10)
    pc.save_img(base_path + 'print_board.jpeg')
    pc.save_pattern_files(base_path + 'pattern/')
    pc.save_mockbot_files(base_path + 'mockbot/', [
        ['00', 3, 1, 37],
        ['01', 0, 0, 0],
        ['02', 2, 3, 90],
        ['03', 3, 2, 180],
        ['04', 1, 5, 270],
        ['05', 1, 7, 123],
        ['06', 7, 3, 10],
        ['07', 3, 1, 222],
        ['08', 4, 9, 300],
        ['09', 2, 5, 115]
    ])
