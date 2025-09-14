import networkx as nx
import self

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodes = DAO.getAllPiloti()
        self._graph = nx.Graph()
        self._idMapPiloti = {}
        for d in self._nodes:
            self._idMapPiloti[d.driverId] = d
    def buildGraph(self):
        self._graph.add_nodes_from(self._nodes)
        self.addAllEdges()

    def addAllEdges(self):
        allEdges = DAO.getAllArchiPiloti(self._idMapPiloti)
        for e in allEdges:
            self._graph.add_edge(e.d1, e.d2, weight=e.peso)

    def hasNode(self, idInput):
        # return idInput in self._graph
        return idInput in self._idMapPiloti

    def getObjectFromId(self, id):
        return self._idMapPiloti[id]

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getInfoConnessa(self, idInput):
        """
        Identifica la componente connessa che
        contiene idInput e ne restituisce la dimensione
        """
        if not self.hasNode(idInput):
            return None

        source = self._idMapPiloti[idInput]

        # Modo1: conto i successori
        succ = nx.dfs_successors(self._graph, source).values()
        res = []
        for s in succ:
            res.extend(s)

        # Modo2: conto i predecessori
        pred = nx.dfs_predecessors(self._graph, source)

        #Modo3: conto i nodi dell'albero di visita
        dfsTree = nx.dfs_tree(self._graph, source)

        #Modo4: uso il metodo nodes_connected_components di networkx
        conn = nx.node_connected_component(self._graph, source)

        return len(conn)

if __name__ == '__main__':
    m = Model()
    m.buildGraph()