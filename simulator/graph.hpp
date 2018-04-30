#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <string>
#include <vector>

struct Node
{
	std::vector<int> edges;
};

class Graph
{
	unsigned int V;
	unsigned int E;
	std::vector<Node> nodes;
public:
	Graph (const std::string &filename);
	void export_graphviz (const std::string &filename) const;
};

#endif // GRAPH_HPP
