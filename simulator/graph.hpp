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
};

#endif // GRAPH_HPP
