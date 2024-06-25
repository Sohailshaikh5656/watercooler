import hashlib
from datetime import datetime

def supplier_token_generator(supplier):
    salt = hashlib.sha256(str(supplier.pk).encode()).hexdigest()[:5]
    hash = hashlib.sha256(str(supplier.pk).encode() + str(salt).encode() + str(datetime.now()).encode()).hexdigest()
    return hash