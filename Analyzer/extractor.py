def extract_id(record):
    """
    Extracts ID from a record dictionary.
    """
    if not record:
        return None
    return record.get("id", "UNKNOWN")

def process_items(items):
    ids = []
    for item in items:
        extracted = extract_id(item)
        if extracted:
            ids.append(extracted)
    return ids
