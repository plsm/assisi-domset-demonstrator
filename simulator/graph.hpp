#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <string>
#include <vector>
#include <set>

struct Node
{
	std::vector<unsigned int> edges;
	bool mark;
};

struct Edge
{
	unsigned int n1, n2;
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
};

#endif // GRAPH_HPP
