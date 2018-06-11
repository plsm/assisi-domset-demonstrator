import argparse
import matplotlib
import matplotlib.pyplot

import assisipy.casu
import CASU_log

def process_arguments ():
    parser = argparse.ArgumentParser (
        description = 'Print the log of a CASU.',
        argument_default = None
    )
    parser.add_argument (
        '--base-path',
        type = str,
        default = '.',
        help = 'path to append to file names'
    )
    parser.add_argument (
        '--casu',
        type = int,
        required = True,
        help = 'CASU number'
    )
    return parser.parse_args ()

def plot (cl):
    # type: (CASU_log.CASU_log) -> None
    figure = matplotlib.pyplot.figure ()
    number_axes = 3
    axes = [figure.add_axes ([0.05, i / float (number_axes) + 0.05, 0.9, (1.0 / number_axes - 0.05)]) for i in range (number_axes)]
    axes [1].scatter (
        [r [0] for r in cl.temp],
        [r [assisipy.casu.TEMP_WAX - assisipy.casu.TEMP_F + 1] for r in cl.temp],
        label = 'wax temperature'
    )
    axes [1].set_ylabel ('temperature (C)')
    for i, c in enumerate (['red', 'green', 'blue']):
        axes [0].scatter (
            [r [0] for r in cl.led],
            [r [1 + i] for r in cl.led],
            label = 'LED',
            c = c,
            marker = '.'
        )
    figure.show ()
    raw_input ('Press ENTER to continue')

def main ():
    args = process_arguments ()
    cl = CASU_log.CASU_log (args.casu, args.base_path)
    plot (cl)

main ()
