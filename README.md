Introduction
============


Apply decision tress to CASUs logs from experiments with Marsela DOMSET algorithm.
Check if an edge is going to become problematic.

Usage
=====

To build the trees.

		python /home/pedro/cloud/git/xSearch/ASSISIbf/plsm/assisi-domset-demonstrator/classifier/build_dataset.py \
			 --condition 7runs- \
			 --base-path ${BASE_PATH} \
			 --graph /media/Adamastor/ASSISIbf/results/domset-interspecies/classifier/graph-doglike \
			 --sampling-time ${SAMPLING_TIME} \
			 --delta-time ${DELTA_TIME} \
			 --temperature-threshold ${TEMPERATURE_THRESHOLD}

Graph file contents

    number_nodes: 5
    edges: [ [N1, N2], [N2, N3], [N2, N5], [N5, N4], [N1, N4]]
    CASU_nodes: {
      N1:[20,21],
      N2:[22,23,24],
      N3:[25],
      N4:[29,30],
      N5:[31,32]
    }
