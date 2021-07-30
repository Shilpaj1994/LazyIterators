"""
Module to return geometric properties of a regular strictly convex polygon using Lazy Iterators
Author: Shilpaj Bhalerao
Date: July 25, 2021
"""
# Standard Library Imports
import math


def lazy_property(func):
    """
    Decorator function for lazy calculations of the property
    :param func: method to be decorator
    :return: closure
    """
    attr_name = "_lazy_" + func.__name__

    @property
    def _lazy_property(self):
        """
        Function to calculate the property if not already done
        :param self: instance
        :return: value of the property
        """
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return _lazy_property


class Polygon:
    """
    Class for lazy properties
    """

    def __init__(self, n, circumradius):
        """
        Constructor
        """
        if n < 3:
            raise ValueError('Polygon must have at least 3 vertices.')
        self._n = n
        self._R = circumradius
        self.cache = dict()

    def __repr__(self):
        """
        Function to print the details of class instance
        """
        return f'Polygon(n={self._n}, R={self._R})'

    @lazy_property
    def count_vertices(self):
        """
        Property to return number of vertices of the regular polygon
        """
        return self._n

    @lazy_property
    def count_edges(self):
        """
        Property to return number of edges of the regular polygon
        """
        return self._n

    @lazy_property
    def circumradius(self):
        """
        Property to return circumradius of the regular polygon
        """
        return self._R

    @lazy_property
    def interior_angle(self):
        """
        Property to return interior angle of the regular polygon
        """
        return (self._n - 2) * 180 / self._n

    @lazy_property
    def side_length(self):
        """
        Property to return length of each side of the regular polygon
        """
        return 2 * self._R * math.sin(math.pi / self._n)

    @lazy_property
    def apothem(self):
        """
        Property to return perpendicular distance from center of circle to side of the regular polygon
        """
        return self._R * math.cos(math.pi / self._n)

    @lazy_property
    def area(self):
        """
        Property to return area of the regular polygon
        """
        return self._n / 2 * self.side_length * self.apothem

    @lazy_property
    def perimeter(self):
        """
        Property to return perimeter of the regular polygon
        """
        return self._n * self.side_length

    def __eq__(self, other):
        """
        Property to implement equality operator for multiple regular polygon
        """
        if isinstance(other, self.__class__):
            return (self.count_edges == other.count_edges
                    and self.circumradius == other.circumradius)
        else:
            return NotImplemented

    def __gt__(self, other):
        """
        Property to implement greater than operator for multiple regular polygon
        """
        if isinstance(other, self.__class__):
            return self.count_vertices > other.count_vertices
        else:
            return NotImplemented


if __name__ == '__main__':
    # Create an instance of a class
    triangle_1 = Polygon(3, 1)
    triangle_2 = Polygon(3, 1)
    square = Polygon(4, 1)

    # Test the __repr__ functionality
    print(f"Repr data: {triangle_1}")

    # Test __eq__ functionality
    print(f"Triangles are same: {triangle_1 == triangle_2}")

    # Test __gt__ functionality
    print(f"Square > Triangle: {square > triangle_2}")

    # Create an instance and access all the properties
    triangle = Polygon(3, 5)
    print(f"Vertices: {triangle.count_vertices}")
    print(f"Edges: {triangle.count_edges}")
    print(f"Circumradius: {triangle.circumradius}")
    print(f"Interior Angle: {triangle.interior_angle}")
    print(f"Side length: {triangle.side_length}")
    print(f"Apothem: {triangle.apothem}")
    print(f"Area: {triangle.area}")
    print(f"Perimeter: {triangle.perimeter}")
