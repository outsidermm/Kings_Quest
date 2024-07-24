def min_max_bound(minimum: int, maximum: int, value: int) -> int:
    """
    Ensures that a given value is bounded within the specified minimum and maximum limits.

    :param minimum: The minimum allowable value.
    :param maximum: The maximum allowable value.
    :param value: The value to be bounded.
    :return: The bounded value, ensuring it is not less than the minimum and not more than the maximum.
    """
    return max(minimum, min(maximum, value))
