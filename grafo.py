from random import choice

class Grafo:

    def __init__(self, dirigido = False):
        self.dirigido = dirigido
        self.cantidad = 0
        self.vertices = {}

    def __len__(self):
        return self.cantidad

    def __iter__(self):
        return(iter(self.vertices.keys()))

    def __str__(self):
        lineas = []
        for vertice, adyacentes in self.vertices.items():
            adyacentes = ["{}-{}".format(ady, peso) for ady, peso in adyacentes.items()]
            lineas.append("{0} : {1}".format(vertice, "  ".join(adyacentes)))
        return '\n'.join(lineas)

    def __repr__(self):
        return str(self)

    def agregar_vertice(self, vertice):
        if vertice not in self.vertices:
            self.vertices[vertice] = {}
            self.cantidad += 1
            return True
        else: return False

    def borrar_vertice(self, vertice):
        if vertice not in self.vertices:
            return False
        else:
            for aristas in self.vertices.values():
                if vertice in aristas:
                    aristas.pop(vertice)
        self.vertices.pop(vertice)
        self.cantidad -= 1
        return True

    def agregar_arista(self, desde, hasta, peso = 1):
        if desde not in self.vertices or hasta not in self.vertices:
            return False
        self.vertices[desde][hasta] = peso
        if not self.dirigido:
            self.vertices[hasta][desde] = peso
        return True

    def borrar_arista(self, vertice, adyacente):
        if vertice in self.vertices and adyacente in self.vertices:
            if adyacente in self.vertices[vertice]:
                self.vertices[vertice].pop(adyacente)
                if not self.dirigido:
                    self.vertices[adyacente].pop(vertice)
                return True
        return False

    def obt_adyacentes(self, vertice):
        if vertice in self.vertices:
            return list(self.vertices[vertice].keys())
        else: return None

    def obt_vertices(self):
        return list(self.vertices.keys())

    def obt_peso(self, v1, v2):
        return self.vertices.get(v1, None).get(v2, None)

    def obt_random(self):
        return choice(list(self.vertices.keys()))