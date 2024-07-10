from uuid import uuid4

def gen_uuid_str():
    """
    Generate uuid and typecast to string for id field
    """
    return str(uuid4())
