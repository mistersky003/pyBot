def validate_int(data, maximum=2147483647, minimum=-2147483647):
    try:
        data = int(data)
        if data < maximum and data > minimum:
            return True, data
        return False, None
    except:
        return False, None
