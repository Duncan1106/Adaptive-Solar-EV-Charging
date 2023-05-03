from time import sleep
from random import random, randint
from shutil import get_terminal_size


def run_progress_bar(total=100, jump_chance=0.15, sleep_time=0.3, block_char='#', space_char=' ', color=None, no_color=False) -> None:
    """
    Prints a progress bar to the console.
    :param total: the total number of units to be processed.
    :param jump_chance: the probability of jumping to 30% progress.
    :param sleep_time: the time to sleep between progress updates (in seconds).
    :param block_char: the character to use for the progress block.
    :param space_char: the character to use for the empty space in the progress bar.
    :param color: the color to use for the progress bar (e.g., "red", "green", "blue", etc.).
    :param no_color: disable color output.
    """

    start = '''
                     _____    ______  __        __     ______
            /\      / ____|  |  ____| \ \      / /    / _____|
           /  \    | (___    | |__     \ \    / /    / /
          / /\ \    \___ \   |  __|     \ \  / /    |  |
         / ____ \   ____) |  | |____     \ \/ /      \  \____
        /_/    \_\ |______/  |______|     \__/        \______|
                Adaptive Solar EV Charging v.9.0 '''
    print (start)

    PROGRESS_JUMP_POINT = 0.3
    PROGRESS_FINISH_POINT = 0.9
    PROGRESS_COMPLETE = 1
    PROGRESS_JUMP_MIN = 1
    PROGRESS_JUMP_MAX = 3
    PROGRESS_INCREASE_MIN = 1
    PROGRESS_INCREASE_MAX = 8
    TERM_WIDTH, _ = get_terminal_size(fallback=(80, 24))

    progress_bar_width = TERM_WIDTH - 15
    block_width = len(block_char)

    if color and not no_color:
        color_start = f"\033[38;5;{color}"
        color_end = "\033[0m"
    else:
        color_start = ""
        color_end = ""

    def update_progress_bar(progress):
        percent = int(progress / total * 100)
        bar_width = int(percent / 100 * progress_bar_width)
        blocks = int(bar_width / block_width)
        spaces = progress_bar_width - blocks
        bar = f'{color_start}[{block_char * blocks}{space_char * spaces}]{color_end}'
        print(f'{bar} {percent}% complete', end='\r')

    progress = 0
    while progress < total:
        # simulate some work being done
        sleep(sleep_time)

        # randomly jump to 30% progress
        if progress < total * PROGRESS_JUMP_POINT and random() < jump_chance:
            progress = int(total * PROGRESS_JUMP_POINT)
        else:
            # progress from 0% to 30%
            if progress < total * PROGRESS_JUMP_POINT:
                progress += randint(PROGRESS_JUMP_MIN, PROGRESS_JUMP_MAX)
            # progress from 30% to 90%
            elif progress < total * PROGRESS_FINISH_POINT:
                progress += randint(PROGRESS_INCREASE_MIN, PROGRESS_INCREASE_MAX)
            # progress from 90% to 100%
            else:
                progress += PROGRESS_COMPLETE

        # update progress bar
        update_progress_bar(progress)

    print(' ')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Prints a progress bar to the console.')
    parser.add_argument('-t', '--total', type=int, default=100, help='the total number of units to be processed')
    parser.add_argument('-j', '--jump-chance', type=float, default=0.15,
                        help='the probability of jumping to 30% progress')
    parser.add_argument('-s', '--sleep-time', type=float, default=0.3,
                        help='the time to sleep between progress updates (in seconds)')
    parser.add_argument('-b', '--block-char', type=str, default='#',
                        help='the character to use for the progress bar blocks')
    parser.add_argument('-p', '--space-char', type=str, default=' ',
                        help='the character to use for the progress bar spaces')
    parser.add_argument('-c', '--color', type=str, default=None,
                        help='the ANSI escape code for the color of the progress bar blocks')
    parser.add_argument('--no-color', action='store_true', help='disable the use of color in the progress bar')

    args = parser.parse_args()

    if not args.no_color and args.color is None:
        args.color = '\033[32m'  # default color to green

    run_progress_bar(args.total, args.jump_chance, args.sleep_time, args.block_char, args.space_char,
                     args.color, args.no_color)