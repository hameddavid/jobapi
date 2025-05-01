import re
import base64 
def is_base64(s):
    # Check if the string length is a multiple of 4
    if len(s) % 4 != 0:
        return False
    # Check if the string only contains valid base64 characters
    if not re.match('^[A-Za-z0-9+/]*={0,2}$', s):
        return False
    try:
        # Try decoding the string to see if it's valid base64
        base64.b64decode(s, validate=True)
    except Exception:
        return False
    return True