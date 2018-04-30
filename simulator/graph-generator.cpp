/**
 * Provides several functions to create diverse family of graphs.
 *
 * Graphs are saved in text files. The first line contains an integer, V,
 * representing the number of vertices, and the second line contains an
 * integer, E, representing the number of edges. Each of the following E lines
 * contain two integers, a number between 1 and V, representing the vertices of
 * an edge.
 *
 * N_V
 * N_E
 * e1v1 e1v2
 * e2v1 e2v2
 * ...
 *
 * @author Pedro Mariano
 * @date 2018, April
 */

#include <sstream>
#include <stdio.h>

#include "graph-generator.h"

using namespace std;

void graph_n_m_star (int n, int m)
{
	ostringstream filename;
	filename << "graph_n-m-star_" << n << "-" << m;
	FILE *fd = fopen (filename.str ().c_str (), "w");
	int V = n + m + 2;
	int E = n + m + 1;
	fprintf (fd, "%d\n%d\n", V, E);
	for (int i = 0; i < n; i++)
		fprintf (fd, "%d %d\n", i + 1, V - 1);
	fprintf (fd, "%d %d\n", V, V - 1);
	for (int i = 0; i < m; i++)
		fprintf (fd, "%d %d\n", i + 1 + n, V);
	fclose (fd);
}
