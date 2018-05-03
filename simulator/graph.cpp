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
	this->edges.push_back (Edge {.n1 = n1, .n2 = n2});
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
	set<unsigned int> sol (v, v + 2);
	result.min_domset.sets.push_back (sol);
	if (n == m) {
		result.min_ind_domset.size = 2;
		for (unsigned int c = 0; c < 2; c++) {
			set<unsigned int> sol;
			sol.insert (c * (m + 1) + n);
			for (unsigned int v = 0; v < n; v++) {
				sol.insert (v + (1 - c) * (n + 1));
			}
			result.min_ind_domset.sets.push_back (sol);
		}
	}
	else {
		result.min_ind_domset.size = 1;
		set<unsigned int> sol;
		if (n < m) {
			sol.insert (m + n + 1);
			for (unsigned int v = 0; v < n; v++) {
				sol.insert (v);
			}
		}
		else {
			sol.insert (n);
			for (unsigned int v = 0; v < m; v++) {
				sol.insert (v + n + 1);
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
		for (unsigned int ein2 : this->nodes [v].edges) {
			if (v < ein2) {
				fprintf (fd, "%d--%d;\n", v, ein2);
			}
		}
	}
	fprintf (fd, "}\n");
	fclose (fd);
}

void Graph::export_solution_graphviz (const set<unsigned int> &solution, const std::string &filename) const
{
	FILE *fd = fopen (filename.c_str (), "w");
	fprintf (fd, "strict graph _ {\n");
	for (unsigned int v = 0; v < this->V; v++) {
		fprintf (fd, "%d", v);
		if (solution.count (v) == 1) {
			fprintf (fd, " [style=bold]");
		}
		fprintf (fd, ";\n");
		for (unsigned int ein2 : this->nodes [v].edges) {
			if (v < ein2) {
				fprintf (fd, "%d--%d;\n", v, ein2);
			}
		}
	}
	fprintf (fd, "}\n");
	fclose (fd);
}

void Graph::export_min_domset_solution_graphviz (unsigned int index, const std::string &filename) const
{
	this->export_solution_graphviz (this->min_domset.sets [index], filename);
}

void Graph::export_min_ind_domset_solution_graphviz (unsigned int index, const std::string &filename) const
{
	this->export_solution_graphviz (this->min_ind_domset.sets [index], filename);
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

void Graph::compute_domset_RSEIDE (gsl_rng *prng, float probability_select_edge)
{
	set<Edge> edges (this->edges.begin (), this->edges.end ());
	while (edges.size () > 0) {
		Edge e = *(edges.begin ());
		edges.erase (edges.begin ());
		if (gsl_rng_uniform (prng) < probability_select_edge) {
			unsigned d1 = (gsl_rng_uniform (prng) < 0.5 ? e.n1 : e.n2);
			this->nodes [d1].mark = true;
			for (unsigned int d2 : this->nodes [d1].edges) {
				edges.erase (Edge (d1, d2));
			}
		}
	}
}
