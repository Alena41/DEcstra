import sys
import networkx as nx
import matplotlib.pyplot as plt


class Graph(object):
    """конструктор класса, принимает координаты вершин и связи между ними, инициализирует атрибуты класса."""
    def __init__(self, coordinates, connections):
        self.coordinates = coordinates
        self.connections = connections
        self.graph = self.construct_graph()

    def construct_graph(self):
        """создает граф на основе переданных координат вершин и связей между ними."""
        graph = {}
        for coord in self.coordinates:
            graph[coord] = {}

        for coord, edges in self.connections.items():
            for adjacent_coord in edges:
                distance = self.calculate_distance(coord, adjacent_coord)
                graph[coord][adjacent_coord] = distance
                graph[adjacent_coord][coord] = distance

        return graph

    def get_distances(self):
        """вычисляет и возвращает расстояния между вершинами в графе."""
        return [self.calculate_distance(coord, adjacent_coord) for coord, edges in self.connections.items() for
                adjacent_coord in edges]

    def get_nodes(self):
        """возвращает список всех вершин графа."""
        return self.graph.keys()

    def get_outgoing_edges(self, coord):
        """возвращает список вершин, с которыми у заданной вершины есть связь."""
        connections = []
        for out_coord in self.graph.keys():
            if self.graph[coord].get(out_coord, False):
                connections.append(out_coord)
        return connections

    def value(self, coord1, coord2):
        """возвращает длину между двумя вершинами."""
        return self.graph[coord1][coord2]

    def draw_graph(self, shortest_path):
        """отрисовывает граф с учетом заданного кратчайшего пути."""
        # создание пустного графа с помощью библиотеки NetworkX
        G = nx.Graph()
        for coord, edges in self.graph.items():
            for adjacent_coord, value in edges.items():
                G.add_edge(coord, adjacent_coord, weight=value)
        # Определение позиций узлов на графе
        pos = {coord: (coord[0], -coord[1]) for coord in self.coordinates}
        # Создание словаря с метками для ребер
        edge_labels = {(coord, adjacent_coord): round(value, 2) for coord, edges in self.graph.items() for
                       adjacent_coord, value
                       in edges.items()}
        # Создание списка ребер для кратчайшего пути
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        # Создание нового графического окна для отображения графа
        plt.figure(figsize=(12, 8))
        # Рисование узлов графа
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold')
        # Добавление меток к ребрам
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='DarkRed')
        # Рисование узлов кратчайшего пути
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_size=2000, node_color='#ffb6c1')
        # Рисование ребер кратчайшего пути
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, node_size=2000, width=10, alpha=0.6, edge_color='#ffb6c2')
        plt.show()

    def dijkstra_algorithm(self, start_coord, end_coord):
        """алгоритм Дейкстры для нахождения кратчайшего пути между двумя заданными вершинами."""
        # получение списка всех узлов в графе
        unvisited_nodes = list(self.get_nodes())

        shortest_path = {}  # хранение длин кратчайших путей до каждого узла
        previous_nodes = {}  # хранение предыдущих узлов на кратчайшем пути

        # задание максимального значения для инициализации длин кратчайших путей
        max_value = sys.maxsize
        # цикл по всем узлам в графе
        for coord in unvisited_nodes:
            #  инициализация длины кратчайшего пути для текущего узла максимальным значением
            shortest_path[coord] = max_value
        shortest_path[start_coord] = 0

        # пока есть непосещенные узлы
        while unvisited_nodes:
            current_min_coord = None  # хранения узла с минимальной длиной пути
            # цикл по непосещенным узлам
            for coord in unvisited_nodes:
                if current_min_coord is None:
                    current_min_coord = coord
                elif shortest_path[coord] < shortest_path[current_min_coord]:
                    current_min_coord = coord

            # получение соседей текущего минимального узла
            neighbors = self.get_outgoing_edges(current_min_coord)
            # цикл по соседям текущего минимального узла
            for neighbor in neighbors:
                # сокращается ли длина пути до соседа через текущий узел
                if shortest_path[current_min_coord] + self.value(current_min_coord, neighbor) < shortest_path[neighbor]:
                    shortest_path[neighbor] = shortest_path[current_min_coord] + self.value(current_min_coord,
                                                                                            neighbor)
                    # сохранение текущего узла как предыдущего для соседа
                    previous_nodes[neighbor] = current_min_coord
            # удаление текущего минимального узла из непосещенных
            unvisited_nodes.remove(current_min_coord)
        path = []  # хранение пути
        coord = end_coord  # назначение конечного узла как текущего узла для построения пути

        # пока текущий узел не станет равен начальному
        while coord != start_coord:
            path.append(coord)
            coord = previous_nodes[coord]

        path.append(start_coord)

        print("Кратчайший путь с длиной {} был найден.".format(shortest_path[end_coord]))
        print(" -> ".join(map(str, reversed(path))))

        return path  # возврат найденного кратчайшего пути

    def calculate_distance(self, coord1, coord2):
        """вычисляет расстояние между двумя координатами точек."""
        x1, y1 = coord1
        x2, y2 = coord2
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distance


# пример использования
# сами координаты
coordinates = [
    (1, 1.5),
    (4, 1.5), (15, 1.5),
    (15, 6.5), (12, 6.5),
    (8, 6.5), (4, 6.5),
    (1, 6.5), (1, 16),
    (6, 16), (7, 13),
    (9, 13), (12, 14),
    (16, 14), (16, 18),
    (12, 18), (9, 18),
    (9, 19.5), (8, 19.5),
    (8, 22), (6, 20),
    (4, 20), (4, 22),
    (10, 22), (10, 24),
    (16, 24), (15, 24)
]

# пути куда можно пойти
connections = {
    (1, 1.5): [(4, 1.5)],
    (4, 1.5): [(15, 1.5), (4, 6.5)],
    (15, 1.5): [(15, 6.5)],
    (15, 6.5): [(12, 6.5)],
    (12, 6.5): [(8, 6.5)],
    (8, 6.5): [(7, 13), (4, 6.5), (9, 13)],
    (7, 13): [(9, 13)],
    (9, 13): [(9, 18)],
    (9, 18): [(9, 19.5), (12, 18)],
    (9, 19.5): [(8, 19.5)],
    (8, 19.5): [(8, 22)],
    (8, 22): [(10, 22)],
    (10, 22): [(10, 24)],
    (10, 24): [(15, 24)],
    (12, 18): [(16, 18)],
    (16, 18): [(16, 24)],
    (16, 24): [(15, 24)],
    (7, 13): [(6, 16)],
    (6, 16): [(6, 20)],
    (6, 20): [(4, 20)],
    (4, 20): [(4, 22)],
    (4, 22): [(8, 22)],
    (4, 6.5): [(1, 6.5)],
    (1, 6.5): [(1, 16)],
    (1, 16): [(6, 16)],
    (12, 14): [(16, 14), (12, 18)],
    (16, 14): [(16, 18)],
}

# вызываются методы для нахождения кратчайшего пути и отрисовки графа с этим путем.
graph = Graph(coordinates, connections)
shortest_path = graph.dijkstra_algorithm((1, 1.5), (15, 24))
graph.draw_graph(shortest_path)
