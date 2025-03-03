from typing import Union


def find_index(value: int, numbers: list[int]) -> Union[int, None]:
    """
    Finds the index of the value in the list withing 10% range.

    It is assumed that the list is sorted in ascending order.
    """

    lower_bound = value * 0.9
    upper_bound = value * 1.1

    closest_index = None
    closest_diff = None

    left, right = 0, len(numbers) - 1

    while left <= right:
        mid = (left + right) // 2
        current_value = numbers[mid]
        prev_value = numbers[mid - 1]

        if lower_bound <= current_value <= upper_bound:
            closest_diff = abs(current_value - value)
            closest_index = mid

        if lower_bound <= prev_value <= upper_bound:
            diff = abs(prev_value - value)
            if closest_diff is None or diff < closest_diff:
                closest_index = mid - 1

        if numbers[mid] < value:
            left = mid + 1
        elif numbers[mid] > value:
            right = mid - 1
        else:
            return mid

    return closest_index if closest_index is not None else None
