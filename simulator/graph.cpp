#include <stdio.h>

#include "graph.hpp"

using namespace std;

Graph::Graph (const string &filename):
   nodes (0)
{
	FILE *fd = fopen (filename.c_str (), "r");
	fscanf (fd, "%u\n%u\n", &this->V, &this->E);
	this->nodes.resize (this->V);
	for (unsigned int i = 0; i < this->E; i++) {
		int ein1, ein2;
		fscanf (fd, "%d %d\n", &ein1, &ein2);
		this->nodes [ein1 - 1].edges.push_back (ein2 - 1);
		this->nodes [ein2 - 1].edges.push_back (ein1 - 1);
	}
	fclose (fd);
}
