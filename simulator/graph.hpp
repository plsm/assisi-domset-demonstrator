#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <string>
#include <vector>

struct Node
{
	std::vector<int> edges;
	bool mark;
};

class Graph
{
	unsigned int V;
	unsigned int E;
	std::vector<Node> nodes;
public:
	Graph (const std::string &filename);
	void export_graphviz (const std::string &filename) const;
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
};

#endif // GRAPH_HPP
