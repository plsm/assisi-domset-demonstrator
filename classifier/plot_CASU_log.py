import argparse
import csv
import matplotlib
import matplotlib.pyplot
import os.path

import assisipy.casu

class CASU_log:
    def __init__ (self, number, base_path = '.'):
        def convert (a):
            if a.find ('.') > -1:
                return float (a)
            else:
                return int (a)
        self.ir_raw = []
        self.temp = []
        self.led = []
        with open (os.path.join (base_path, 'casu-{:03d}.csv'.format (number)), 'r') as fd:
            reader = csv.reader (fd, delimiter=';', quoting = csv.QUOTE_MINIMAL)
            for row in reader:
                if row [0] == 'ir_raw':
                    self.ir_raw.append ([convert(x) for x in row [1:]])
                elif row [0] == 'temp':
                    self.temp.append ([convert(x) for x in row [1:]])
                elif row [0] == 'DiagnosticLed':
                    self.led.append ([convert(x) for x in row [1:]])
                #       Airflow
            # DiagnosticLed
            # dled_ref
            # fft_amp
            # fft_freq
            # ir_range
            # ir_raw
            # Peltier
            # Peltier_temp
            # Speaker
            # temp
            # VibrationPattern
            fd.close ()

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
    cl = CASU_log (args.casu, args.base_path)
    plot (cl)

main ()
