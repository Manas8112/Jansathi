def extract_placeholders(text: str) -> list[str]:
    import re
    found = re.findall(r'\[([A-Z][A-Z ]+)\]', text)
    return list(dict.fromkeys(found))  # deduplicated, order preserved
