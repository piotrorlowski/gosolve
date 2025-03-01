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

    current_num = numbers[idx]
    previous_num = numbers[idx - 1]

    # Check if the element at the found index is within the bounds
    if lower_bound <= current_num <= upper_bound:
        closest_diff = abs(current_num - value)
        closest_index = idx

    # Check the previous element to see if it's closer
    if lower_bound <= previous_num <= upper_bound:
        diff = abs(previous_num - value)
        if closest_diff is None or diff < closest_diff:
            closest_index = idx - 1

    return closest_index if closest_index is not None else None
