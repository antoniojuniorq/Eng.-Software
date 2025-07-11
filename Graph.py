import random

class Edge:
    def __init__(self, target, weight):
        self.target = target
        self.weight = weight

class Vertex:
    def __init__(self, name):
        self.name = name
        self.adjacents = []

    def addEdge(self, target, weight):
        self.adjacents.append(Edge(target, weight))

class Graph:
    def __init__(self):
        self.vertices = {}

    def addVertex(self, name):
        if name not in self.vertices:
            self.vertices[name] = Vertex(name)

    def addEdge(self, source, target, weight):
        self.addVertex(source)
        self.addVertex(target)
        self.vertices[source].addEdge(target, weight)

    def findPathWithDistance(self, source, target, visited=None, path=None, distance=0):
        if visited is None:
            visited = set()
        if path is None:
            path = []

        if source in visited:
            return None

        visited.add(source)
        path.append(source)

        if source == target:
            return path.copy(), distance

        for edge in self.vertices[source].adjacents:
            result = self.findPathWithDistance(edge.target, target, visited, path, distance + edge.weight)
            if result:
                return result

        path.pop()
        return None

graph = Graph()

locais_fixos = ["Garagem", "Secretaria de Saúde", "CAF", "CEMURF", "UPA SUL", "UPA NORTE"]

graph.addEdge("Garagem", "Secretaria de Saúde", 4)
graph.addEdge("Secretaria de Saúde", "CAF", 6)
graph.addEdge("Secretaria de Saúde", "CEMURF", 5)
graph.addEdge("CAF", "UPA SUL", 8)
graph.addEdge("CEMURF", "UPA NORTE", 9)

unidades = []
for i in range(1, 33):
    unidade = f"Unidade {i}"
    unidades.append(unidade)
    destino = random.choice(["UPA SUL", "UPA NORTE", "CAF", "CEMURF"])
    graph.addEdge(unidade, destino, random.randint(5, 20))
    origem = random.choice(["Garagem", "UPA SUL", "UPA NORTE", "CAF", "CEMURF"])
    graph.addEdge(origem, unidade, random.randint(5, 15))

todos_os_locais = locais_fixos + unidades

origem = "Garagem"

print("\n\nSIMULADOR DE DESLOCAMENTO ENTRE DEPARTAMENTOS DE SAÚDE DE PALMAS")
print("\nOrigem inicial fixa em 'Garagem'.")
print("Digite 'sair' para encerrar.\n")

while True:
    print(f"\nOrigem atual: {origem}")
    print("Locais disponíveis para DESTINO:")
    for nome in todos_os_locais:
        if nome != origem:
            print(nome)

    destino = input(f"\nEscolha o DESTINO a partir de '{origem}' (ou 'sair'): ").strip()
    if destino.lower() == "sair":
        break
    if destino not in graph.vertices:
        print("Destino inválido. Tente novamente.")
        continue

    resultado = graph.findPathWithDistance(origem, destino)
    if resultado:
        caminho, distancia_total = resultado
        print("\nCaminho encontrado:")
        print(" → ".join(caminho))
        print(f"Distância total: {distancia_total} km")
    else:
        print("Nenhum caminho encontrado entre os locais informados.")

    origem = destino
