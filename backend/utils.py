import re
import html


def sanitize_string(text: str) -> str:
    """
    Cleans a string by escaping HTML and removing control characters.

    Args:
        text (str): The input string to sanitize.

    Returns:
        str: The sanitized string.
    """
    if not isinstance(text, str):
        return ""

    # Escape HTML entities (e.g., <script> becomes &lt;script&gt;)
    escaped = html.escape(text)

    # Remove control characters and other suspicious invisible chars
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", escaped)

    # Optionally, trim long whitespace or weird characters
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
