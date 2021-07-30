"""
Module for Lazy Iterable Implementation
Author: Shilpaj Bhalerao
Date: July 25, 2021
"""
# Local Imports
from goal_1 import Polygon


class Polygons:
    """
    Iterable for regular polygons
    """
    def __init__(self, circumradius):
        """
        Constructor
        :param circumradius: radius of a circle in which the polygons are inscribed in
        """
        if circumradius < 0:
            raise ValueError('R must be greater than 0')
        self._m = 2
        self._R = circumradius
        self._instance = None

    def __iter__(self):
        """
        Method to make this class Iterable
        :return: Instance of the Iterator class
        """
        self._instance = self.PolygonIterator(self)
        return self._instance

    class PolygonIterator:
        """
        Iterator class for the Iterable
        """
        def __init__(self, obj):
            """
            Constructor
            """
            self._obj = obj
            self._ratio_data = dict()
            self.collection = []

        def __iter__(self):
            """
            Method to make this class Iterator
            """
            return self

        def __next__(self):
            """
            Method to iterate over the values of iterator
            """
            # Increment the number of edges
            self._obj._m += 1

            # Create a polygon with number of edges and circumradius
            polygon = Polygon(self._obj._m, self._obj._R)

            # Calculate the ratio using the porperties of the polygon
            ratio = polygon.area / polygon.perimeter

            # Keep a record of edges and ratio
            if self._obj._m not in self._ratio_data:
                self._ratio_data[self._obj._m] = ratio

            # Append all the polygon instances
            self.collection.append(polygon)

            return polygon

        @property
        def ratio_data(self):
            """
            Property to access ratio of area to perimeter of all the polygon
            """
            return self._ratio_data

        @property
        def get_collection(self):
            """
            Property to access instances of all the polygons
            """
            return self.collection

    def __len__(self):
        """
        Method to print the number of polygons in an instance
        """
        return len(self._instance.ratio_data)

    def __repr__(self):
        """
        Method to print information of collections
        """
        return f'Collection of regular Polygons from edges 3 to {len(self._instance.ratio_data) + 2}'

    def __getitem__(self, index):
        """
        Method to access the polygons using slicing and indexing
        """
        if isinstance(index, int):
            if index < 0:
                index = len(self._instance.ratio_data) + index
            if index < 0 or index > len(self._instance.ratio_data):
                raise IndexError
            else:
                return self._instance.get_collection[index]
        else:
            start, stop, step = index.indices(len(self._instance.ratio_data))
            rng = range(start, stop, step)
            return [self._instance.get_collection[index] for index in rng]

    @property
    def max_efficiency_polygon(self):
        """
        Property to access the number of edges of a polygon with maximum area to perimeter ratio
        """
        sorted_polygons = sorted(self._instance.ratio_data, reverse=True)
        return sorted_polygons[0]


if __name__ == '__main__':
    # Create instance of Lazy Iterable
    polys = Polygons(circumradius=5)

    # Access the Lazy Iterator
    polys_iter = iter(polys)

    # Test Iterator functionality
    for _ in range(20):
        polygon = next(polys_iter)
        print(f"Edges: {polygon.count_edges}")

    # Test __repr__ functionality
    print(f"Repr data: {polys}")

    # Test __len__ functionality
    print(f"Length: {len(polys)}")

    # Test Indexing functionality
    print(f"Indexing: {polys[::-1]}")

    # Test Slicing functionality
    print(f"Slicing: {polys[2:5:1]}")

    # Test maximum efficiency functionality
    print(f"Max efficiency: {polys.max_efficiency_polygon}")
