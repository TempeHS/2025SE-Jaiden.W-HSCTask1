import html
import re


# Sanitize a dictionary of data by escaping HTML characters.
def sanitize_data(data):
    sanitized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized_data[key] = html.escape(value)
        else:
            sanitized_data[key] = value
    return sanitized_data

#Sanitize an input string by removing unwanted characters and escaping HTML characters.
def sanitize_input(input_string):
    sanitized_string = re.sub(r'[^\w\s-]', '', input_string) 
    sanitized_string = html.escape(sanitized_string)  
    return sanitized_string