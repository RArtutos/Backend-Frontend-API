"""
Utility functions for parsing and handling cookie strings
"""

def parse_cookie_string(cookie_string: str) -> list:
    """Parse a cookie string into a list of cookie dictionaries"""
    if not cookie_string:
        return []
        
    cookies = []
    for cookie_part in cookie_string.split(';'):
        cookie_part = cookie_part.strip()
        if not cookie_part:
            continue
            
        try:
            name, value = cookie_part.split('=', 1)
            cookies.append({
                'name': name.strip(),
                'value': value.strip(),
                'domain': None,  # Will be set by the form
                'path': '/'
            })
        except ValueError:
            continue  # Skip malformed cookies
            
    return cookies