import argparse
import csv
import os.path
import yaml

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
        with open (os.path.join (base_path, 'casu-{:03d}.csv'.format (number)), 'r') as fd:
            reader = csv.reader (fd, delimiter=';', quoting = csv.QUOTE_MINIMAL)
            for row in reader:
                if row [0] == 'ir_raw':
                    self.ir_raw.append ([convert(x) for x in row [1:]])
                elif row [0] == 'temp':
                    self.temp.append ([convert(x) for x in row [1:]])
            ## self.data = [[row[0]] + [convert(x) for x in row [1:]] for row in reader]
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

class Node:
    def __init__ (self, list_casu_numbers, dict_CASU_logs):
        self.CASU_logs = dict ([(c, dict_CASU_logs [c]) for c in list_casu_numbers])
        self.number_CASUs = float (len (list_casu_numbers))
        print (self.CASU_logs)

    def highest_smallest_time (self):
        return max ([c.highest_smallest_time () for c in self.CASU_logs.values ()])

    def temperature (self, time):
        values = [c.temperature (time) for c in self.CASU_logs.values ()]
        if None in values:
            return None
        else:
            return sum (values) / self.number_CASUs

    def infrared (self, time):
        values = [c.infrared (time) for c in self.CASU_logs.values ()]
        if None in values:
            return None
        else:
            return sum (values) / self.number_CASUs


class Edge:
    def __init__ (self, nodes, dict_nodes):
        print (nodes)
        self.nodes = (dict_nodes [nodes [0]], dict_nodes [nodes [1]])
        print (self.nodes)

    def build_data_set (self, sampling_time, delta_time, temperature_threshold):
        print ('Computing data set for edge {} {}'.format (self.nodes [0], self.nodes [1]))
        current_time = max (self.nodes [0].highest_smallest_time (), self.nodes [1].highest_smallest_time ())
        result = []
        print ('Computing build data starting from time {}'.format (current_time))
        go = True
        while go:
            record_attributes = [
                self.nodes [0].temperature (current_time),
                self.nodes [1].temperature (current_time),
                self.nodes [0].infrared (current_time),
                self.nodes [1].infrared (current_time)
            ]
            if None in record_attributes:
                go = False
            else:
                # compute class
                t1, t2 = self.nodes [0].temperature (current_time + delta_time), self.nodes [1].temperature (current_time + delta_time)
                if t1 is None or t2 is None:
                    go = False
                else:
                    record_class = [t1 > temperature_threshold and t2 > temperature_threshold]
                    record = record_class + record_attributes
                    result.append (record)
                    current_time += sampling_time

        return result

def process_arguments ():
    parser = argparse.ArgumentParser (
        description = 'Process CASU logs and graph specification in order to build a data set to be used by the classifier.',
        argument_default = None
    )
    parser.add_argument (
        '--base-path',
        type = str,
        default = '.',
        help = 'path to append to file names'
    )
    parser.add_argument (
        '--graph', '-g',
        type = str,
        required = True
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

def main ():
    args = process_arguments ()
    with open (args.graph, 'r') as fd:
        graph = yaml.load (fd)
    CASUs = [c for n in graph ['CASU_nodes'] for c in graph ['CASU_nodes'][n] ]
    CASU_logs = dict ([(c, CASU_log (c, args.base_path)) for c in CASUs])
    nodes = dict ([(n, Node (graph ['CASU_nodes'] [n], CASU_logs)) for n in graph ['CASU_nodes']])
    edges = [Edge (ns, nodes) for ns in graph ['edges']]

    dataset = []
    for e in edges:
        dataset.extend (e.build_data_set (args.sampling_time, args.delta_time, args.temperature_threshold))
    print (dataset)
    with open ('data-set_st={}_dt={}_tt={}'.format (args.sampling_time, args.delta_time, args.temperature_threshold), 'w') as fd:
        writer = csv.writer (fd, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
        writer.writerows (dataset)


main ()
