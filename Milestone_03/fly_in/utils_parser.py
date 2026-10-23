def parse_metadata_functional(
    meta_str: str, valid_keys: set[str]
) -> dict[str, str]:
    if not meta_str.strip():
        return {}

    tokens = meta_str.split()
    bad = [t for t in tokens if "=" not in t]
    if bad:
        raise ValueError(f"Malformed metadata token(s): {bad}")

    pairs = [tuple(map(str.strip, t.split("=", 1))) for t in tokens]
    invalid_keys = [k for k, _ in pairs if k not in valid_keys]
    if invalid_keys:
        raise ValueError(
            f"Invalid metadata key(s): {invalid_keys}. "
            f"Expected one of {sorted(valid_keys)}"
        )
    return {k: v for k, v in pairs}


def extract_statement_data(right_part: str) -> tuple[str, str]:
    start_idx = right_part.find("[")

    if start_idx == -1:
        return right_part.strip(), ""

    end_idx = right_part.find("]")
    if end_idx == -1 or end_idx < start_idx:
        raise ValueError(
            f"Mal-formed metadata block in '{right_part}': "
            "missing closing ']'"
        )

    data_part = right_part[:start_idx].strip()
    meta_part = right_part[start_idx + 1:end_idx].strip()
    return data_part, meta_part
