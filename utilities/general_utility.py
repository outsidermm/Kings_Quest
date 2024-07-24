def min_max_bound(minimum: int, maximum: int, value: int) -> int:
    """
    Ensures that a given value is bounded within the specified minimum and maximum limits.

    :param minimum: The minimum allowable value.
    :param maximum: The maximum allowable value.
    :param value: The value to be bounded.
    :return: The bounded value, ensuring it is not less than the minimum and not more than the maximum.
    """
    return max(minimum, min(maximum, value))


def convert_snake_to_title(string: str) -> str:
    """
    Converts a snake_case string to Title Case.

    This function takes a string in snake_case format, splits it into individual words,
    capitalizes each word, and then joins them with spaces to form a Title Case string.

    Example:
        >>> convert_snake_to_title("hello_world_example")
        'Hello World Example'

    Args:
        string (str): The snake_case string to be converted.

    Returns:
        str: The converted Title Case string.
    """
    return " ".join(word.capitalize() for word in string.split("_"))
