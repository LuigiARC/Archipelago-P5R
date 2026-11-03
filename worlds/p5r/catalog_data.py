import json


def catalog_bytes(document: dict) -> bytes:
    return (json.dumps(document, indent=2) + "\n").encode("utf-8")
