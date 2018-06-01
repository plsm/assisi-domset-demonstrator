# This module provides a class that represents an edge classifier. Given the
# state of an edge it tells if that edge is going to be problematic.


import argparse
import pickle

class SimpleEdgeClassifier:
    """
    An edge classifier that given a tuple with the temperature and the
    average infrared readings of the two nodes of an edge tells if that
    edge is going to be problematic.

    This edge classifier assumes that all models were trained with a
    data set with four attributes: the first two are the temperatures of
    the two nodes in ascending order; the last two attributes are the
    average infrared values of the nodes in ascending order.

    This edge classifier does NOT assume that the models that uses were
    all trained with the same data sets, sampling time, temperature
    threshold and delta time.
    """
    def __init__ (self, list_file_names_model):
        """
        Construct a simple edge classifier using the models in the files.

        :param list_file_names_model: List with file names were models are saved.
        """
        self.models = []
        for a_filename in list_file_names_model:
            print ('Reading decision trees in file {}'.format (a_filename))
            with open (a_filename, 'rb') as fd:
                go = True
                while go:
                    try:
                        self.models.append (pickle.load (fd))
                    except EOFError:
                        go = False
                    except Exception as e:
                        print (e)
        print ('Using {} models'.format (len (self.models)))

    def is_edge_problematic (self, temperature_1, temperature_2, average_infrared_1, average_infrared_2):
        """
        Performs an election among the models to see if the edge is OK
        or is going to become problematic.

        :param temperature_1:
        :param temperature_2:
        :param average_infrared_1:
        :param average_infrared_2:

        :return: A tuple containing a boolean value indicating if the edge is
        going to become problematic and the number of votes obtained by
        the OK side and problem side.

        :rtype: (bool,int,int)
        """
        attributes = [[
            min (temperature_1, temperature_2),
            max (temperature_1, temperature_2),
            min (average_infrared_1, average_infrared_2),
            max (average_infrared_1, average_infrared_2)
        ]]
        votes_OK = 0
        votes_KO = 0
        for a_tree in self.models:
            answer = a_tree.predict (attributes)
            if answer == [1]:
                votes_OK +=1
            elif answer == [0]:
                votes_KO += 1
        return votes_KO > votes_OK, votes_OK, votes_KO

def main ():
    args = parse_arguments ()
    classifier = SimpleEdgeClassifier (args.filename)
    for t1 in args.temperature:
        for t2 in args.temperature:
            for ir1 in args.average_infrared:
                for ir2 in args.average_infrared:
                    print (t1, t2, ir1, ir2, classifier.is_edge_problematic (t1, t2, ir1, ir2))

def parse_arguments ():
    parser = argparse.ArgumentParser (
        description = 'Test the edge classifier.  Reads decision trees and given a set of temperatures and average infrared values, returns the classification by the decision trees.',
        argument_default = None
    )
    parser.add_argument (
        'filename',
        nargs = '+',
        help = 'filename with processed CASU log data'
    )
    parser.add_argument (
        '--temperature', '-t',
        type = float,
        required = True,
        action = 'append',
        help = 'node temperature'
    )
    parser.add_argument (
        '--average-infrared', '-i',
        type = float,
        required = True,
        action = 'append',
        help = 'node temperature'
    )
    return parser.parse_args ()

if __name__ == '__main__':
    main ()
