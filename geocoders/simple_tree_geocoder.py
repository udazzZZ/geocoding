from api import API, TreeNode
from geocoders.geocoder import Geocoder


# Перебор дерева
class SimpleTreeGeocoder(Geocoder):
    def __init__(self, samples: int | None = None, data: list[TreeNode] | None = None):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data

    def _apply_geocoding(self, area_id: str) -> str:
        """
            TODO:
            - Сделать перебор дерева для каждого area_id
            - В ходе перебора возвращать массив элементов, состоящих из TreeNode необходимой ветки
            - Из массива TreeNode составить полный адрес
        """

        def dfs(node, visited=None):
            if visited is None:
                visited = set()
            visited.add(node.id)

            if int(node.id) == int(area_id):
                return node.name
            else:
                for n in node.areas:
                    if n.id not in visited:
                        next = dfs(n, visited)
                        if next:
                            return node.name + ', ' + next

        for item in self.__data:
            address = dfs(item)
            if address:
                return str(area_id) + ',"' + address + '"'
