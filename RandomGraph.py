import random
import copy
""" All graphs in this code are represented as NxN matrices. Each NxN matrix correpsonds to a graph with N vertices with V = {0,1,...N}
Within each Matrix, a 1 at the ith,jth entry represents an edge between vertex i and j,
and a 0 at the ith,jth entry significies that no edge exists between vertex i and j. Each (i,i) is a 0.

"""


def isConnected_Neighobrhood(graph):
	# takes a graph, and returns a True/False value whether the Graph is True or False
	C_set = set()
	def addToSet(graph,vertex):
		for i in range(len(graph[0])):
			if graph[vertex][i] == 1 and  i not in C_set:
				C_set.add(i)
				addToSet(graph,i)
	addToSet(graph,0)
	if len(C_set) == len(graph[0]):
		return True
	else:
		return False

"""def generate_connected_Graph(edge, vertex):
	# Much slower than the algorithm below 


	 give the number of edges and vertices (int) that you want a graph to have and this will return a graph as such subject to 
	 	vertex - 1 <= edge  <= (vertex) * (vertex -1)/2  if edge < vertex -1 or edge > vertex * (vertex -1)/2 : 
	 	return error	 	if edge < vertex - 1 or edge > vertex*(vertex - 1)/2:
		print("Invalid number of edges")
		return None
	graph = generate_Graph(edge,vertex)
	while not isConnected_Neighobrhood(graph):
		graph = generate_Graph(edge,vertex)
	return graph"""


def generate_connected_Graph_PruferCode(edge,vertex):
	# this code generates a random connected graph by generating a random prufer code, and then adding edges to the tree 'skeleton'
	# Not uniformly distributed unfortunately, as can be proved 

	if edge < vertex - 1 or edge > vertex*(vertex - 1)/2:
		print("Invalid number of edges")
		return None
	PrufCode = []
	for i in range(vertex-2):
		PrufCode.append(random.randint(0,vertex-1))
		#here we create a random prufer code which will be the 'tree skeleton' of our random connected graph
	G = Refurp(PrufCode)
	E = generate_edge_set(G)
	edge = edge - vertex - 1 #the tree skeleton uses vertex -1 edges 
	while edge >0:
		x = True
		while x:
			a = random.randint(0,vertex-1)
			b = random.randint(0,vertex-1)
			if not a == b and not G[a][b] ==1:
				x = False
		G[a][b] = 1
		G[b][a] = 1
		edge = edge -1
	return G


def generate_Graph(edge, vertex):
	""" input the number of edges and vertices in a graph
	and it will output a graph in matrix form """
	if edge > vertex *(vertex -1)/2 or vertex <0 or edge < 0:
		print("Invalid number of edges")
		return None

	graph = [[0 for x in range(vertex)] for y in range(vertex)] 
	
	
	while edge >0:
		a = random.randint(0,vertex-1)
 
		b = random.randint(0,vertex-1)

		if  graph[a][b] == 1 or a ==b: 
			continue

		else: 
			
			edge = edge -1
			graph[a][b] = 1
			graph[b][a] = 1
	return graph


def generate_edge_set(graph):
	#generates the edge set of a given graph 
	# NOTE, the Edge Set generated is a LIST, not a SET 
	edge_set = []
	for i in range(len(graph[0])):
		for j in range(len(graph[0])):
			if graph[i][j] == 1 and i != j:
				edge_set.append((i,j))
	return edge_set

def degree_sequences(graph):
	# takes in a graph, and returns a dictionary that are the degree sequences of the graph
	degree_seq = {}
	for j in range(len(graph[0])):
		count = 0 
		for i in range(len(graph[0])):
			if graph[j][i] == 1 and j != i:
				count = count +1
		degree_seq[j] = count
	return degree_seq


def isThereCycle(graph):
	#returns a boolean value for whether there is a cycle 
	# for each edge in a graph, this takes out the edge and checks if the graph is still connected
	#if the graph is still connected, then there must be a cycle within the original graph
	E = generate_edge_set(graph)
	for edge in E:
		tempgraph = graph[:]
		tempgraph[edge[0]][edge[1]] = 0
		tempgraph[edge[1]][edge[0]] = 0
		if isConnected_Neighobrhood(tempgraph):
			return True
	return False
def probabilityConnected_disconnect_Edge(graph, disconnections):

	# given a graph G, this returns the probability that given X random edge-disconnections, the graph is connected
	edge_set = generate_edge_set(graph)

	count =0
	if len(edge_set)/2 < disconnections:
		return None 
	for j in range(10000):
		E = list(edge_set)
		tempgraph = copy.deepcopy(graph)
		for i in (range(disconnections)):
			a = random.randint(0,len(E)-1)
			edge = E[a]
			tempgraph[edge[0]][edge[1]] = 0
			tempgraph[edge[1]][edge[0]] = 0
			E.remove((edge[0],edge[1]))
			E.remove((edge[1],edge[0]))
		if not isConnected_Neighobrhood(tempgraph):
			count = count +1 
	return(1-count/10000)


def Kruskals_Algorithm(graphh,weight): 
	# input a graph and a weight dictionary -- edge:weight 
	# this will return a minimum-cost spanning tree

	graph = copy.deepcopy(graphh)
	tree = [[0 for x in range(graph[0])] for y in range(graph[0])] 
	E = set(generate_edge_set(graph)) 

	def findMinEdge(edge_set):
		minEdge = (0,0)
		for e in edge_set:
			if weight[e] < weight[minEdge]:
				minEdge = e
		return minEdge
	while len(E) != 0:
		e = findMinEdge(E)
		f = (e[1].e[0])
		TempTree = tree[:]
		TempTree[e[0]][e[1]], TempTree[e[1][0]] = 1
		E.remove(e)
		E.remove(f)
		if not isThereCycle(TempTree):
			tree = TempTree[:]
	return tree


def PruferCode(g):
	#input a tree, and the computer returns the prufer code -- starting with vertex 0

	graph = copy.deepcopy(g)
	num_vertex = len(graph[0])
	Code = []
	def LeafSet(graph):
		#returns set of leaves in a graph
		degreeSequences = degree_sequences(graph)
		L = []
		for i in range(len(degreeSequences)):
			if degreeSequences[i] == 1:
				L.append(i)
				L.sort()
		return L
	def Leaf_neighbor(vertex,graph):
		#given a graph and a vertex that is a leaf, this returns the leaf's neighbor
		s = 0
		for i in range(len(graph[vertex])):
			if graph[vertex][i] == 1:
				s = i
				break
		return s
		
		
	while num_vertex >2:
		
		L = LeafSet(graph)
		v = Leaf_neighbor(L[0],graph)
		Code.append(v)
		graph[L[0]][v] = 0
		graph[v][L[0]] = 0
		num_vertex = num_vertex -1
	return Code


def Refurp(PC):
	# takes a PruferCode list and spits out a graph that correpsponds to that prufer code
	PruferCode = PC.copy()
	T = [[0 for x in range(len(PruferCode)+2)] for y in range(len(PruferCode)+2)]  
	def LeafSet(Code):
		L = []
		for i in range(len(Code)+2):
			if Code.count(i) == 0:
				L.append(i)
		L.sort()
		return L
	x = 0
	L = LeafSet(PruferCode)
	while len(PruferCode)>0:
		T[L[0]][PruferCode[0]]=1
		T[PruferCode[0]][L[0]] = 1
		x = PruferCode[0]
		PruferCode.pop(0)
		L.pop(0)
		if x not in PruferCode:
			L.append(x)
			L.sort()

	T[L[0]][L[1]]=1
	T[L[1]][L[0]] =1
	return T

def edge_distance(A, B, graphh):
	# tells the number of edges betwen A and B in graph G
	graph = copy.deepcopy(graphh)
	def Generate_NeighborhoodSet(vertex,graph):
		N = set()
		for i in range(len(graph[vertex])):
			if graph[vertex][i] == 1:
				N.add(i)
		return N

	
	if A == B: 
		return 0
	void_set = {A}
	W = Generate_NeighborhoodSet(A,graph)
	count =1
	V = set(range(len(graph[0])))
	placeholder = set()
	while B not in W and not void_set == V:
		for vertices in W :
			if vertices in void_set:
				continue
			placeholder = set.union(placeholder,(Generate_NeighborhoodSet(vertices,graph)))
		void_set = set.union(void_set,W)
		W = set.intersection(placeholder,V-void_set)
		count = count +1
	if void_set == V:
		return None
	return count


def print_Graph(graph):
	for w in range(0,len(graph[0])):
		for x in range(0, len(graph[0])):
			print(str(graph[w][x]))
		print("next row")


def D_shortestPath(weight, graph, a, b):
	#djikstra's shortest path algorithm given a weight and two vertices a,b with graph 
	def Generate_NeighborhoodSet(vertex,graph):
		N = set()
		for i in range(len(graph[vertex])):
			if graph[vertex][i] == 1:
				N.add(i)
		return N
	def find_smallestVert(Unused_set, golden_distence):
		vertex = 0
		for x in Unused_set:
			if x not in golden_distence:
				continue
			try: 
				if golden_distence[x] < golden_distence[0]:
					vertex = x
			except KeyError:
				vertex = x
		return x



	unused = set(range(0,len(graph[0])))
	current = a
	golden_distence = {a:0}



	while b in unused:
		neighbors = Generate_NeighborhoodSet(current, graph)
		for y in neighbors:
			try:
				if golden_distence[y] > weight[(current,y)] + golden_distence[x]:
					golden_distence[y]  = weight[(current,y)] + golden_distence[x]
			except KeyError: 
				golden_distence[y] = weight[(current,y)] + golden_distence[x]
		unused.remove(current)
		
		current = find_smallestVert(Unused_set, golden_distence)
		if b == current:
			break


