from hashlib import md5

def md5_hash(cleaned_psd: bytes) -> str:
    return md5(cleaned_psd).hexdigest()