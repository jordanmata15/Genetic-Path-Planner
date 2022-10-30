from __future__ import annotations
from typing import List

import math

class Home:

    def __init__(self, index_pair, home_index):
        self.xy_index = index_pair
        self.home_index = home_index


    def distance_to(self, index: List[int, int]):
        """Calculates the Euclidean distance from this house to 
        another pair of indices.

        Args:
            index (List[int, int]): The index to calculate the distance to.

        Returns:
            float: The distance from the calling home to another index.
        """
        x_delta = self.xy_index[0] - index[0]
        y_delta = self.xy_index[1] - index[1]
        return math.sqrt(x_delta**2 + y_delta**2)
        

    def __eq__(self, other: Home) -> bool:
        """Determines if two homes are equal. Used for validating chromosomes.

        Args:
            other (Home): Home to compare to.

        Returns:
            bool: True if the calling home is equal to the passed in home.
        """
        if self.home_index == other.home_index and self.xy_index == other.xy_index:
            return True
        else:
            return False