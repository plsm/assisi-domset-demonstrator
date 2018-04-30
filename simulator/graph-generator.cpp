/**
 * Provides several functions to create diverse family of graphs.
 *
 * These families have well known solutions to the minimum dominating set and
 * the minumum independent dominating set problems. As such we also provide the
 * solutions to these problems.
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
 * After the grap description comes the solutions to the MINDOMSET and
 * MIN-IND-DOMSET problems. The first line of this section contains a character
 * representing the type of solution: C for complete and S for a summary. The
 * second line contains two integers, S_D and S_I, representing the size of the
 * MIN-DOMSET and MIN-IND-DOMSET problems, respectively. In case of a complete
 * solution, the next line contains a number, N_D, representing how many
 * solutions exist for the MIN-DOMSET problems. The next N_D lines all contain
 * S_D integers that represent a node of a solution. Afterwards comes a line
 * with a single number, N_I, representing how many solutions exist for the
 * MIN-IND-DOMSET problems. Each of the following N_I lines contain S_I
 * integers that represent a node of a solution.
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
	fprintf (fd, "C\n2 %d\n", 1 + min (n, m));
	fprintf (fd, "1\n%d %d\n", V - 1, V);
	if (n == m) {
		fprintf (fd, "2\n");
		for (int i = 0; i < n; i++)
			fprintf (fd, "%d ", i + 1);
		fprintf (fd, "%d\n", V);
		for (int i = 0; i < n; i++)
			fprintf (fd, "%d ", i + 1 + n);
		fprintf (fd, "%d\n", V - 1);
	}
	else {
		fprintf (fd, "1\n");
		if (n < m) {
			for (int i = 0; i < n; i++)
				fprintf (fd, "%d ", i + 1);
			fprintf (fd, "%d\n", V);
		}
		else {
			for (int i = 0; i < m; i++)
				fprintf (fd, "%d ", i + 1 + n);
			fprintf (fd, "%d\n", V - 1);
		}
	}
	fclose (fd);
}
