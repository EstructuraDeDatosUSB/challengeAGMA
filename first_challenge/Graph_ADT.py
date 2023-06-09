import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64
matplotlib.use('Agg')

# Para crear un TDA de grafos simples, es necesario primero saber de que esta compuesto un grafo simple
# Un grafo simple esta compuesto por un conjunto de vertices y un conjunto de aristas
# Por ende para modelar el TDA es necesario entenderlo como una clase que contenga una lista de adyacencia
# Con lista de adyasencia me refiero a una lista de listas, donde cada lista interna representa un vertice

# TDA de Grafos Simples

class Graph:
    """
    Esta clase representa la estructura de un grafo simple. 

    Attributes:
        adjacentList (dict): Un diccionario que contiene como llaves los vertices del grafo 
            y como valores una lista de los vertices adyacentes a cada vertice.

    Methods:
    addVertex(vertex): Agrega un nuevo vertice al grafo.
    addEdge(vertex1, vertex2): Agrega una arista entre dos vertices del grafo.
    getNeighbors(vertex): Retorna la lista de vertices adyacentes a un vertice dado.
    __str__(): Retorna una representacion en string del grafo.
    """

    def __init__(self, directed=False, weighted=False):
        """
        Inicializa un grafo simple.

        Args:
        directed (bool): Indica si el grafo es dirigido o no.
        weighted (bool): Indica si el grafo es ponderado o no.
        """
        self.adjacentList = {}
        self.directed = directed
        self.weighted = weighted

    def addVertex(self, vertex):
        """
        Agrega un vertice al grafo.

        Args:
        vertex (int or str): El vertice a agregar.
        """
        if vertex not in self.adjacentList:
            self.adjacentList[vertex] = []

    def addEdge(self, src, dest, weight=None):
        """
        Agrega una arista entre dos vertices del grafo.

        - Si es dirigido, entonces se agrega un vertice a la lista de adyacencia del otro vertice,
        pero el otro vertice no se agrega a la lista de adyacencia del vertice actual.
        - Si es no dirigido, entonces se agrega un vertice a la lista de adyacencia del otro vertice,
        y el otro vertice tambien se agrega a la lista de adyacencia del vertice actual.

        - Si es ponderado, entonces se agrega el peso de la arista entre los dos vertices.

        Args:
        challengeAGMA (any): El vertice de origen.
        dest (any): El vertice de destino.
        weight (int or None): El peso de la arista. Si el grafo es ponderado, este argumento es obligatorio.

        Raises:
        ValueError: Si el grafo es ponderado y no se proporciona un peso para la arista.

        """
        if src not in self.adjacentList:
            self.addVertex(src)
        if dest not in self.adjacentList:
            self.addVertex(dest)

        if self.weighted and weight is None:
            raise ValueError(
                "Este grafo es ponderado, se debe proporcionar un peso para la arista.")
        elif not self.weighted:
            weight = None

        self.adjacentList[src].append((dest, weight))

        if not self.directed:
            self.adjacentList[dest].append((src, weight))

    def getVertices(self):
        """
        Retorna la lista de vertices del grafo.

        Returns:
        list: La lista de vertices del grafo.
        """
        return list(self.adjacentList.keys())

    def getNeighbors(self, vertex):
        """
        Retorna la lista de vertices adyacentes a un vertice dado.

        Args:
        vertex (any): El vertice del que se quieren obtener los vertices adyacentes.

        Returns:
        list: La lista de vertices adyacentes al vertice dado.
        """
        return self.adjacentList[vertex]

    def getWeight(self, src, dest):
        """
        Retorna el peso de la arista entre dos vertices dados.

        Args:
        challengeAGMA (any): El vertice de origen.
        dest (any): El vertice de destino.

        Returns:
        int: El peso de la arista entre los dos vertices dados.
        """
        for neighbor, weight in self.adjacentList[src]:
            if neighbor == dest:
                return weight

    # =================== BFS (Breadth First Search) ===================
    
    def bfs(self, start):
        """
        Realiza un recorrido BFS (Breadth First Search / Busqueda en Anchura) del grafo.

        Args:
        start (any): El vertice de inicio del recorrido.

        Returns:
        list: La lista de vertices en el orden en el que fueron visitados.
        """
        visited = []
        queue = [start]

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.append(vertex)
                for neighbor, weight in self.adjacentList[vertex]:
                    queue.append(neighbor)
        return visited

    def bfs_shortest_path(self, start, end):
        """
        Retorna el camino mas corto entre dos vertices dados,
        utilizando un recorrido BFS (Breadth First Search / Busqueda en Anchura)

        Args:
        start (any): El vertice de inicio del recorrido.
        end (any): El vertice de fin del recorrido.

        Returns:
        list: La lista de vertices en el orden en el que fueron visitados.
        """
        visited = []
        queue = [[start]]
        while queue:
            path = queue.pop(0)
            vertex = path[-1]
            if vertex not in visited:
                visited.append(vertex)
                for neighbor, weight in self.adjacentList[vertex]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    if neighbor == end:
                        return new_path
        
    # =====================================================================
    
    # =================== DFS (Depth First Search) ===================
    
    def dfs(self, start, end, avoid):
        """
        Realiza un recorrido DFS (Depth First Search / Busqueda en profundidad) del grafo.

        Args:
        start (any): El vertice de inicio del recorrido.
        end (any): El vertice de destino del recorrido.
        avoid (any): El vertice que se debe evitar en el camino.

        Returns:
        list: La lista de vertices en el orden en el que fueron visitados, sin incluir el vértice prohibido.
        """
        path = {start: None}
        stack = [start]

        while stack:
            vertex = stack.pop()
            if vertex == end:
                break
            for neighbor, weight in self.adjacentList[vertex]:
                if neighbor == avoid:
                    continue
                if neighbor not in path:
                    path[neighbor] = vertex
                    stack.append(neighbor)

        if end not in path:
            return []

        # Construir la ruta desde el inicio al destino
        current = end
        route = [current]
        while current != start:
            current = path[current]
            route.append(current)
        route.reverse()

        return route

    
    def dfs_shortest_path(self, start, end):
        """
        Retorna el camino mas corto entre dos vertices dados,
        utilizando el algoritmo de DFS (Depth First Search / Busqueda en profundidad)

        Args:
        start (any): El vertice de inicio del recorrido.
        end (any): El vertice de fin del recorrido.

        Returns:
        list: La lista de vertices en el orden en el que fueron visitados.
        """
        visited = []
        stack = [[start]]

        while stack:
            path = stack.pop()
            vertex = path[-1]
            if vertex not in visited:
                visited.append(vertex)
                for neighbor, weight in self.adjacentList[vertex]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.append(new_path)
                    if neighbor == end:
                        return new_path
        
    # =====================================================================
    
    # =================== Dijkstra ===================
    
    def dijkstra(self, start, end):
        """
        Retorna el camino mas corto entre dos vertices dados,
        utilizando el algoritmo de Dijkstra.

        Args:
        start (any): El vertice de inicio del recorrido.
        end (any): El vertice de fin del recorrido.

        Returns:
        list: La lista de vertices en el orden en el que fueron visitados.
        """
        distances = {}
        previous = {}
        queue = []
        path = []
        
        for vertex in self.adjacentList:
            if vertex == start:
                distances[vertex] = 0
                heapq.heappush(queue, [0, vertex])
            else:
                distances[vertex] = float("inf")
                heapq.heappush(queue, [float("inf"), vertex])
            previous[vertex] = None

        while queue:
            current = heapq.heappop(queue)[1]
            if current == end:
                while previous[current]:
                    path.append(current)
                    current = previous[current]
                break
            if current in self.adjacentList:
                for neighbor, weight in self.adjacentList[current]:
                    alternative = distances[current] + weight
                    if alternative < distances[neighbor]:
                        distances[neighbor] = alternative
                        previous[neighbor] = current
                        for i in range(len(queue)):
                            if queue[i][1] == neighbor:
                                queue[i][0] = alternative
                                break
                        heapq.heapify(queue)
        result = path[::-1]
        result.insert(0, start)
        return result
    
    
    def visualize(self):
        """
        Visualiza el grafo utilizando la libreria networkx.
        """
        g_nx = nx.DiGraph()

        # Agregamos los nodos al grafo de NetworkX
        for node in self.getVertices():
            g_nx.add_node(node)

        # Agregamos las aristas al grafo de NetworkX
        for node in self.getVertices():
            neighbors = self.getNeighbors(node)
            for neighbor in neighbors:
                g_nx.add_edge(node, neighbor[0])

        # Visualizamos el grafo
        nx.draw(g_nx, with_labels=True)
        plt.show()
        
    def draw_graph(self):
        """
        Draw the graph using the NetworkX library with a circular layout.
        """
        G = nx.DiGraph() if self.directed else nx.Graph()

        # Add vertices
        G.add_nodes_from(self.getVertices())

        # Add edges
        for vertex in self.adjacentList:
            for neighbor, weight in self.adjacentList[vertex]:
                G.add_edge(vertex, neighbor, weight=weight)

        # Use circular layout
        pos = nx.circular_layout(G)

        # Draw nodes and edges
        nx.draw_networkx_nodes(G, pos, node_size=500)
        nx.draw_networkx_edges(G, pos)

        # Add node labels
        labels = {v: v for v in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels)

        # Add edge labels
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        plt.clf()

        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return image_base64








    def __str__(self):
        """
        Retorna una representacion en string del grafo.

        Returns:
        str: Una representacion en string del grafo.
        """
        result = ""
        for vertex in self.adjacentList:
            result += f"[{vertex}] -----> "
            neighbors = []
            for neighbor, weight in self.adjacentList[vertex]:
                if weight is not None:
                    neighbors.append(f"[{neighbor}] [{weight}]")
                else:
                    neighbors.append(f"[{neighbor}]")
            result += ", ".join(neighbors)
            result += "\n"
        return result
