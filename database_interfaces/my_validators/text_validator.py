def validate_text(data, max_count_chars, min_count_chars, need_keys=()):
    if data is not None:
        data = str(data)
        if len(data) < max_count_chars and len(data) > min_count_chars:
            for need_key in need_keys:
                if need_key[0] != "$":
                    need_key = "$" + need_key
                if not need_key in data:
                    return False, None
            return True, data
    return False, None
