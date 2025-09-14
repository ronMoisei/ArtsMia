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

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

if __name__ == '__main__':
    m = Model()
    m.buildGraph()