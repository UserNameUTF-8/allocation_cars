import hashlib


def sha256(pass_: str):
    hasher_ = hashlib.sha256()
    hasher_.update(pass_.encode())
    return hasher_.hexdigest()
