from api import TreeNode, API
from geocoders.geocoder import Geocoder


# Инверсия дерева
class MemorizedTreeGeocoder(Geocoder):
    def __init__(self, samples: int | None = None, data: list[TreeNode] | None = None):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data
        self.addresses = {}

        def dfs(node, visited=None):
            if visited is None:
                visited = set()
            visited.add(node.id)
            self.addresses[node.id].append(node.name)

            for n in node.areas:
                if n.id not in visited:
                    self.addresses[n.id] = self.addresses[node.id].copy()
                    dfs(n, visited)

        for i in self.__data:
            self.addresses[i.id] = []
            dfs(i)

    """
        TODO:
        Сделать функцию перебора дерева:
        - Для каждого узла сохранять в словарь адресов
    """

    def _apply_geocoding(self, area_id: str) -> str:
        """
            TODO:
            - Возвращать данные из словаря с адресами
        """
        return str(area_id) + ',"' + ', '.join(self.addresses[str(area_id)]) + '"'


