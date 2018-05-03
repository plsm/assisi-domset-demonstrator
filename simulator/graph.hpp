#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <string>
#include <vector>
#include <set>
#include <gsl/gsl_rng.h>

struct Node
{
	std::vector<unsigned int> edges;
	bool mark;
};

struct Edge
{
	unsigned int n1, n2;
	Edge (unsigned int n1, unsigned int n2):
	   n1 (std::min (n1, n2)),
	   n2 (std::max (n1, n2))
	{}
	bool operator< (const Edge e) const
	{
		return this->n1 < e.n1 || (this->n1 == e.n1 && this->n2 < e.n2);
	}
};

struct Solution
{
	unsigned int size;
	std::vector<std::set<unsigned int> > sets;
};

class Graph
{
	unsigned int V;
	unsigned int E;
	std::vector<Node> nodes;
	std::vector<Edge> edges;
	Solution min_domset;
	Solution min_ind_domset;
	void add_edge (unsigned int n1, unsigned int n2);
	void export_solution_graphviz (const std::set<int unsigned> &solution, const std::string &filename) const;
public:
	Graph (unsigned int V);
	Graph (const std::string &filename);
	void export_graphviz (const std::string &filename) const;
	/**
	 * @brief export_solution_graphviz Create a graphviz file with one of the
	 * solutions of the minimum independent dominating set problem.
	 *
	 * @param index
	 * @param filename
	 */
	void export_min_domset_solution_graphviz (unsigned int index, const std::string &filename) const;
	void export_min_ind_domset_solution_graphviz (unsigned int index, const std::string &filename) const;
	/**
	 * @brief is_min_domset Checks if the marked nodes constitute a dominating set
	 * of this graph.
	 *
	 * @return true if the marked nodes constitute a dominating set of this graph.
	 */
	bool is_domset () const;
	/**
	 * @brief is_independent_domset Checks if marked nodes constitue an
	 * independent dominanting set of this graph.
	 *
	 * A subset S of the vertices of graph G is an independent dominating set, if
	 * no two vertices of S are an edge of graph G, AND the set of vertices
	 * adjacent to any vertex in S plus set S constitue the vertices of graph G.
	 *
	 * @return true if the marked nodes constitute an independent dominanting set
	 * of this graph.
	 */
	bool is_independent_domset () const;
	static Graph generate_n_m_star (unsigned int n, unsigned int m);
	/**
	 * @brief compute_domset_RSEIDE Randomly select an edge, pick one of its nodes
	 * and inhibit the departing edges.
	 *
	 * This algorithm goes through all edges. An edge can be processed depending on
	 * probability <i>p</i>.
	 *
	 * Processing an edge means: select one of its nodes; inhibit the departing
	 * edges from being processed.
	 *
	 * @param prng
	 * @param probability_select_edge
	 */
	void compute_domset_RSEIDE (gsl_rng *prng, float probability_select_edge);
};

#endif // GRAPH_HPP
