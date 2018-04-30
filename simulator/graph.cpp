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

void Graph::export_graphviz (const string &filename) const
{
	FILE *fd = fopen (filename.c_str (), "w");
	fprintf (fd, "strict graph _ {\n");
	for (unsigned int v = 0; v < this->V; v++) {
		fprintf (fd, "%d", v);
		if (this->nodes [v].mark) {
			fprintf (fd, " [style=bold]");
		}
		fprintf (fd, ";\n");
		for (int ein2 : this->nodes [v].edges) {
			if (v < ein2) {
				fprintf (fd, "%d--%d;\n", v, ein2);
			}
		}
	}
	fprintf (fd, "}\n");
	fclose (fd);
}

bool Graph::is_domset () const
{
	vector<bool> marked (this->V);
	for (unsigned int v = 0; v < this->V; v++) {
		if (this->nodes [v].mark) {
			marked [v] = true;
			for (int ein2 : this->nodes [v].edges) {
				marked [ein2] = true;
			}
		}
	}
	for (bool v : marked) {
		if (!v) {
			return false;
		}
	}
	return true;
}
