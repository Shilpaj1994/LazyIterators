"""
Module containing test cases for the Polygons class
Author: Shilpaj Bhalerao
Date: July 25, 2021
"""
# Standard Library Imports
from collections.abc import Iterator, Iterable

# Local Imports
from goal_1 import Polygon
from goal_2 import Polygons


def is_iterable(obj) -> bool:
    """
    Function to check if an object is iterable
    """
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def test_polygons_iterable():
    """
    Test case to check if Polygons is Iterable
    """
    polys = Polygons(circumradius=5)
    assert is_iterable(polys)
    assert not isinstance(polys, Iterator)


def test_repr_implementation():
    """
    Test case to check if __repr__ is implemented
    """
    polys = Polygons(circumradius=5)
    assert '__repr__' in dir(polys)


def test_len_implementation():
    """
    Test case to check if __len__ is implemented
    """
    polys = Polygons(circumradius=5)
    assert '__len__' in dir(polys)


def test_indexing():
    """
    Test case to check if indexing is implemented
    """
    # Create instance of Lazy Iterable
    polys = Polygons(circumradius=5)

    # Access the Lazy Iterator
    polys_iter = iter(polys)

    # Test Iterator functionality
    for _ in range(20):
        polygon = next(polys_iter)

    assert polys[0] == Polygon(3, 5)


def test_slicing():
    """
    Test case to check if slicing is implemented
    """
    # Create instance of Lazy Iterable
    polys = Polygons(circumradius=5)

    # Access the Lazy Iterator
    polys_iter = iter(polys)

    # Test Iterator functionality
    for _ in range(20):
        polygon = next(polys_iter)

    assert polys[0:2] == [Polygon(3, 5), Polygon(4, 5)]


def test_max_efficiency():
    """
    Test case to check if maximum efficiency polygon is correct
    """
    # Create instance of Lazy Iterable
    polys = Polygons(circumradius=5)

    # Access the Lazy Iterator
    polys_iter = iter(polys)

    # Test Iterator functionality
    for _ in range(20):
        polygon = next(polys_iter)

    assert polys.max_efficiency_polygon == 22