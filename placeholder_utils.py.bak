import re


def extract_placeholders(text: str) -> list[str]:
    """
    Finds all uppercase-word placeholders of the form [SOME PLACEHOLDER]
    in a drafted document and returns them deduplicated, in order.
    """
    found = re.findall(r'\[([A-Z][A-Z ]+)\]', text)
    return list(dict.fromkeys(found))  # deduplicated, order preserved
