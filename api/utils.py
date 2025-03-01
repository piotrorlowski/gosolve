from typing import Union


def find_index(value: int, numbers: list[int]) -> Union[int, None]:
    """
    Finds the index of the value in the list withing 10% range.

    It is assumed that the list is sorted in ascending order.
    """
    lower_bound = value * 0.9
    upper_bound = value * 1.1

    left, right = 0, len(numbers) - 1
    closest_index = -1
    closest_diff = None

    while left <= right:
        mid = (left + right) // 2
        mid_value = numbers[mid]

        # If mid_value is within the 10% range, check if it's closer to the target
        if lower_bound <= mid_value <= upper_bound:
            diff = abs(mid_value - value)
            if closest_diff is None or diff < closest_diff:
                closest_diff = diff
                closest_index = mid

        if mid_value < value:
            left = mid + 1
        elif mid_value > value:
            right = mid - 1
        else:
            return mid

    return closest_index if closest_index != -1 else None
