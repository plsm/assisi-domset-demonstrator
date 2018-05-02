#include <stdio.h>

#include "graph.hpp"

using namespace std;

Graph::Graph (unsigned int V):
   V (V),
   E (0),
   nodes (V)
{
}

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

void Graph::add_edge (unsigned int n1, unsigned int n2)
{
	this->E++;
	this->nodes [n1].edges.push_back (n2);
	this->nodes [n2].edges.push_back (n1);
}

Graph Graph::generate_n_m_star (unsigned int n, unsigned int m)
{
	Graph result (n + m + 2);
	for (unsigned int i = 0; i < n; i++) {
		result.add_edge (i, n);
	}
	for (unsigned int i = 0; i < m; i++) {
		result.add_edge (i + n + 1, m + n + 1);
	}
	result.add_edge (n, m + n + 1);
	result.min_domset.size = 1;
	unsigned int v[] = {n, m + n + 1};
	set<unsigned int> sol (v, v + 1);
	result.min_domset.sets.push_back (sol);
	if (n == m) {
		result.min_ind_domset.size = 2;
		for (unsigned int c = 0; c < 2; c++) {
			set<unsigned int> sol;
			sol.push_back (c * (m + 1) + n);
			for (unsigned int v = 0; v < n; v++) {
				sol.push_back (v + (1 - c) * (n + 1));
			}
			result.min_ind_domset.sets.push_back (sol);
		}
	}
	else {
		result.min_ind_domset.size = 1;
		set<unsigned int> sol;
		if (n < m) {
			sol.push_back (m + n + 1);
			for (unsigned int v = 0; v < n; v++) {
				sol.push_back (v);
			}
		}
		else {
			sol.push_back (n);
			for (unsigned int v = 0; v < m; v++) {
				sol.push_back (v + n + 1);
			}
		}
		result.min_ind_domset.sets.push_back (sol);
	}
	return result;
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

bool Graph::is_independent_domset () const
{
	vector<bool> marked (this->V);
	for (unsigned int v = 0; v < this->V; v++) {
		if (this->nodes [v].mark) {
			marked [v] = true;
			for (int ein2 : this->nodes [v].edges) {
				if (this->nodes [ein2].mark) {
					return false;
				}
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
