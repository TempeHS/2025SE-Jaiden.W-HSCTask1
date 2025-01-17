import html

def sanitize_data(data):
    sanitized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized_data[key] = html.escape(value)
        else:
            sanitized_data[key] = value
    return sanitized_data