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
  edges: [ [1, 2], [2, 3], [2, 5], [5, 4], [1, 4]]
  CASU_nodes: {
  1:[20,21],
  2:[22,23,24],
  3:[25],
  4:[29,30],
  5:[31,32]
  }
