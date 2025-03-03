from typing import Union


def binary_search(value: int, numbers: list[int]) -> int:
    left, right = 0, len(numbers)
    while left < right:
        mid = (left + right) // 2
        if numbers[mid] < value:
            left = mid + 1
        else:
            right = mid
    return left


def find_index(value: int, numbers: list[int]) -> Union[int, None]:
    """
    Finds the index of the value in the list withing 10% range.

    It is assumed that the list is sorted in ascending order.
    """
    idx = binary_search(value, numbers)

    lower_bound = value * 0.9
    upper_bound = value * 1.1

    closest_index = None
    closest_diff = None

    try:
        current_value = numbers[idx]
        prev_value = numbers[idx - 1]

        if lower_bound <= current_value <= upper_bound:
            closest_diff = abs(current_value - value)
            closest_index = idx

        if lower_bound <= prev_value <= upper_bound:
            diff = abs(prev_value - value)
            if closest_diff is None or diff < closest_diff:
                closest_index = idx - 1

        return closest_index if closest_index is not None else None
    except IndexError:
        return None
