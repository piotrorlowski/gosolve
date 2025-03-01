import bisect
from typing import Union


def find_index(value: int, numbers: list[int]) -> Union[int, None]:
    """
    Finds the index of the value in the list within a 10% range.

    It is assumed that the list is sorted in ascending order.
    """
    lower_bound = value * 0.9
    upper_bound = value * 1.1

    # Use bisect to find the closest possible index
    idx = bisect.bisect_left(numbers, value)

    closest_index = None
    closest_diff = None

    # Check if the element at the found index is within the bounds
    if idx < len(numbers) and lower_bound <= numbers[idx] <= upper_bound:
        closest_index = idx
        closest_diff = abs(numbers[idx] - value)

    # Check the previous element to see if it's closer
    if idx > 0 and lower_bound <= numbers[idx - 1] <= upper_bound:
        diff = abs(numbers[idx - 1] - value)
        if closest_diff is None or diff < closest_diff:
            closest_index = idx - 1
            closest_diff = diff

    return closest_index if closest_index is not None else None
