import csv
import os.path

import assisipy.casu

class CASU_log:
    """
    List of CASU log data that is not parsed in the current version of this class:

    Airflow
    DiagnosticLed
    dled_ref
    fft_amp
    fft_freq
    ir_range
    ir_raw
    Peltier
    Peltier_temp
    Speaker
    temp
    VibrationPattern
    """
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
            fd.close ()

    def highest_smallest_time (self):
        return max ([self.ir_raw [0][0], self.temp [0][0]])

    def temperature (self, time):
        index = CASU_log.__binary_search_time (self.temp, time)
        if index == len (self.temp):
            return None
        else:
            return self.temp [index][assisipy.casu.TEMP_WAX - assisipy.casu.TEMP_F + 1]

    def infrared (self, time):
        index = CASU_log.__binary_search_time (self.ir_raw, time)
        if index == len (self.ir_raw):
            return None
        else:
            return sum (self.ir_raw [index][1:7]) / 6.0

    @staticmethod
    def __binary_search_time (data, time):
        low = 0
        high = len (data)
        while low + 1 < high:
            middle = low + (high - low) / 2
            if data [middle][0] == time:
                return middle
            elif data [middle][0] < time:
                low = middle
            else:
                high = middle
        return low
