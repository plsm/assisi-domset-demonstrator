import argparse
import collections
import csv
import datetime
import numpy
import os.path
import pickle
import stat
import sklearn.neural_network
import sklearn.tree
import time
import yaml

import dataset

def main ():
    args = parse_arguments ()
    seed = int (time.time ()) if args.RNG_seed is None else args.RNG_seed
    RNG = numpy.random.RandomState (seed)
    data_sets = dataset.load_data_sets (args.data_sets)
    suffix = filename_suffix (args, seed)

    parameters = load_decision_tree_parameters (args.learning_parameters)
    results_file, results_writer = open_decision_tree_results (suffix)
    NN_file = open_decision_tree_file (suffix)
    for index in range (args.number_repeats):
        run_decision_tree (RNG, args.fraction_test, data_sets, parameters, results_writer, NN_file, index)
    results_file.close ()
    NN_file.close ()

def parse_arguments ():
    parser = argparse.ArgumentParser (
        description = "Optigrape worker"
    )
    parser.add_argument (
        "--data-sets",
        metavar = "PATH",
        type = str,
        required = True,
        help = "text file containing pairs of data sets and their classes."
    )
    parser.add_argument (
        "--fraction-test",
        type = float,
        required = True,
        metavar = "X",
        help = "Fraction of the data set to be used as test set"
    )
    parser.add_argument (
        "--learning-parameters",
        metavar = "PATH",
        type = str,
        required = True,
        help = "text file containing the parameters of the classifier algorithm."
    )
    parser.add_argument (
        "--RNG-seed",
        type = int,
        default = None,
        metavar = "N",
        help = "Pseudo-random number generator seed, if not present uses current time"
    )
    parser.add_argument (
        "--number-repeats",
        type = int,
        default = 30,
        metavar = "N",
        help = "how many repeats to perform"
    )
    return parser.parse_args ()

def load_decision_tree_parameters (parameters_filename):
    with open (parameters_filename, "r") as fd:
        dictionary = yaml.load (fd)
        result = dictionary ["decision_tree"]
        print ("Parameters of the decision tree: {0}".format (result))
        return result


def run_decision_tree (RNG, fraction_test, data_sets, parameters, results_writer, DT_fd, index_repeat):
    print ("I'm going to run decision tree")
    train, test = dataset.split_data_sets_train_test (data_sets, fraction_test, RNG)
    clf = sklearn.tree.DecisionTreeClassifier (
        criterion = parameters ["criterion"],
        max_depth = parameters ["max_depth"],
        min_samples_split = parameters ["min_samples_split"],
        random_state = RNG
    )
    current_time, score, hit = run_classifier (clf, train, test)
    write_decision_tree_results (results_writer, current_time, index_repeat, parameters, score, hit)
    write_decision_tree_structure (DT_fd, clf)

def run_classifier (classifier, train, test):
    current_time = time.time ()
    classifier.fit (train.xs, train.ys)
    ys = classifier.predict (test.xs)
    score = compute_score (ys, test.ys)
    print ("Score is {0}".format (score))
    hit = random_chance_to_hit (train, test)
    return current_time, score, hit

def compute_score (classifier_ys, test_ys):
    score = 0
    false_positive = 0
    false_negative = 0
    for an_y, a_test_y in zip (classifier_ys, test_ys):
        if isinstance (a_test_y, collections.Iterable):
            if all ([ay == at for ay, at in zip (an_y, a_test_y)]):
                score += 1
        else:
            score += 1 if an_y == a_test_y else 0
            if an_y != a_test_y:
                if a_test_y == 0:
                    false_positive += 1
                else:
                    false_negative += 1
    return [score / float (len (test_ys)), false_positive / float (len (test_ys) - score), false_negative / float (len (test_ys) - score)]

def random_chance_to_hit (train, test):
    # type: (dataset.Function, dataset.Function) -> float
    """
    Compute the chance of a random classifier to correctly classify a sample in the test set, given a training set.
    :param test:
    :type train: dataset.Function
    :type test: dataset.Function
    """
    def compute_classes_occurrence (l):
        # type: (collections.Iterable) -> dict
        r = {}
        for x in l:
            if x in r:
                r [x] = r [x] + 1
            else:
                r [x] = 1
        return r
    count_classes_train = compute_classes_occurrence (train.IDs)
    count_classes_test = compute_classes_occurrence (test.IDs)
    result = sum ([count_classes_train [key] * count_classes_test [key] for key in count_classes_test.keys ()])
    result = result / float (len (train.IDs) * len (test.IDs))
    return result

def filename_suffix (args, seed):
    # type: (argparse.Namespace) -> str
    data = datetime.datetime.now ().__str__().split ('.') [0]
    data = data.replace (' ', '-').replace (':', '-')
    result = "{0}_{1}_{2}_{3}_{4}".format (
        os.path.basename (args.data_sets),
        os.path.basename (args.learning_parameters),
        seed,
        args.fraction_test,
        data
    )
    return result

def open_results_file (suffix, parameters):
    # type: (str, dict) -> object
    results_file = open ("results_{0}.csv".format (suffix), "w")
    results_writer = csv.writer (results_file, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
    header_row = [
        "time",
        "run",
        "activation",
        'solver',
        "alpha",
        'early.activation',
        'max.iterations'
    ] + [
        'hidden.layer.{0:d}.size'.format (index + 1) for index in range (len (parameters ["hidden_layers_size"]))
    ] + [
        "num.iterations",
        "score",
        "random.chance.win"
    ]
    results_writer.writerow (header_row)
    return results_file, results_writer

def open_neural_network_file (suffix):
    NN_file = open ("neural-network_{0}.csv".format (suffix), "w")
    NN_writer = csv.writer (NN_file, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
    return NN_file, NN_writer

def write_results (results_writer, current_time, index_repeat, parameters, clf, score, hit):
    row = [
        current_time,
        index_repeat,
        parameters ["activation"],
        parameters ["solver"],
        parameters ["alpha"],
        parameters ["early_stopping"],
        parameters ["max_iterations"]
    ] + parameters ["hidden_layers_size"] + [
        clf.n_iter_,
        score,
        hit
    ]
    results_writer.writerow (row)

def write_neural_network (NN_writer, current_time, index_repeat, clf):
    row = [current_time, index_repeat, clf.out_activation_, clf.n_layers_, clf.n_outputs_]
    for matrix in clf.coefs_:
        for cr in matrix:
            row.extend (cr)
    for r in clf.intercepts_:
        row.extend (r)
    NN_writer.writerow (row)

def open_decision_tree_results (suffix):
    # type: (str, dict) -> object
    results_file = open ("decision-tree_results_{0}.csv".format (suffix), "w")
    results_writer = csv.writer (results_file, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
    header_row = [
        "time",
        "run",
        "criterion",
        'max.depth',
        "min.samples.split",
        "random.chance.win"
        "score",
        "false.positive",
        "false.negative"
    ]
    results_writer.writerow (header_row)
    return results_file, results_writer

def open_decision_tree_file (suffix):
    DT_file = open ("decision-tree_structure_{0}.csv".format (suffix), "wb")
    return DT_file

def write_decision_tree_results (results_writer, current_time, index_repeat, parameters, score, hit):
    row = [
        current_time,
        index_repeat,
        parameters ["criterion"],
        parameters ["max_depth"],
        parameters ["min_samples_split"],
        hit
    ] + score
    results_writer.writerow (row)

def write_decision_tree_structure (DT_file, classifier):
    pickle.dump (classifier, DT_file)

main ()
