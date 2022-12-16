def escape_single_quote_value(d: dict) -> dict:
    """
    This method escapes single quote to all the values
    """
    for k, v in d.items():
        if type(v) == list:
            d[k] = '{"' + '","'.join(v).replace("'", "''") + '"}'

        elif type(v) == str:
            d[k] = v.replace("'", "''")
    return d
