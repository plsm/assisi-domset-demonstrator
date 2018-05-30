import argparse
import csv
import os
import stat

def process_arguments ():
    parser = argparse.ArgumentParser (
        description = 'Process CASU logs and graph specification in order to build a data set to be used by the classifier.',
        argument_default = None
    )
    parser.add_argument (
        'filename',
        nargs = '+',
        help = 'filename with processed CASU log data'
    )
    parser.add_argument (
        '--delta-time',
        type = float,
        required = True,
        help = 'Time between sensor readings and edge classification'
    )
    parser.add_argument (
        '--sampling-time',
        type = float,
        required = True,
        help = 'Sampling time used when processing CASU sensor readings to create data set'
    )
    parser.add_argument (
        '--temperature-threshold',
        type = float,
        required = True,
        help = 'Smallest temperature that the CASUs in an edge have to have in order for that edge to be considered problematic.'
    )
    return parser.parse_args ()


def convert (a):
    if a.find ('.') > -1:
        return float (a)
    else:
        return int (a)

def what_to_write (row):
    temperature_1 = row [2]
    temperature_2 = row [3]
    infrared_1 = row [4]
    infrared_2 = row [5]
    return [
        min (temperature_1, temperature_2),
        max (temperature_1, temperature_2),
        min (infrared_1, infrared_2),
        max (infrared_1, infrared_2)
    ]

def main ():
    args = process_arguments ()
    data_set_ok_filename = 'class-OK_st={}_dt={}_tt={}.csv'.format (
        args.sampling_time,
        args.delta_time,
        args.temperature_threshold
    )
    fd_ok = open (data_set_ok_filename, 'w')
    data_set_ko_filename = 'class-KO_st={}_dt={}_tt={}.csv'.format (
        args.sampling_time,
        args.delta_time,
        args.temperature_threshold
    )
    fd_ko = open (data_set_ko_filename, 'w')
    writer_ok = csv.writer (fd_ok, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
    writer_ok.writerow (['temperature.1', 'temperature.2', 'infrared.1', 'infrared.2'])
    writer_ko = csv.writer (fd_ko, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
    writer_ko.writerow (['temperature.1', 'temperature.2', 'infrared.1', 'infrared.2'])
    for file_name in args.filename:
        with open (file_name, 'r') as fd_:
            print ('Processing {}...'.format (file_name))
            reader = csv.reader (fd_, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
            reader.next ()
            for row in reader:
                #what_to_write = [convert(x) for x in row [2:]]
                attributes = what_to_write (row)
                if row [1] == 'KO':
                    writer_ko.writerow (attributes)
                elif row [1] == 'OK':
                    writer_ok.writerow (attributes)
            fd_.close ()
    fd_ok.close ()
    fd_ko.close ()
    os.chmod (data_set_ok_filename, stat.S_IRUSR)
    os.chmod (data_set_ko_filename, stat.S_IRUSR)

main ()
