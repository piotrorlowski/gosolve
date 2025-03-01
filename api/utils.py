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
        prev_mid_value = numbers[mid - 1]

        if lower_bound <= mid_value <= upper_bound:
            closest_diff = abs(mid_value - value)
            closest_index = mid

        if lower_bound <= prev_mid_value <= upper_bound:
            diff = abs(prev_mid_value - value)
            if closest_diff is None or diff < closest_diff:
                closest_index = mid - 1

        if mid_value < value:
            left = mid + 1
        elif mid_value > value:
            right = mid - 1
        else:
            return mid

    return closest_index if closest_index != -1 else None
