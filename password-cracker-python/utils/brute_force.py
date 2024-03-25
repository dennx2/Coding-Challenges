from hashlib import md5
from itertools import permutations
import string


def brute_force(hashed_psd: str) -> str | None:
    letters = string.ascii_letters + string.punctuation + string.digits
    for i in range(6, 11):
        for perm in permutations(letters, i):
            combi = "".join(perm)
            combi_byte = combi.encode()
            combi_hash = md5(combi_byte).hexdigest()
            if combi_hash == hashed_psd:
                return combi
    return None