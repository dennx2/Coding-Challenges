from itertools import permutations
import string

from .timer_decorator import timer
from .hash_function import md5_hash

@timer
def brute_force(hashed_psd: str) -> str | None:
    letters = string.ascii_letters + string.punctuation + string.digits
    for i in range(6, 11):
        for perm in permutations(letters, i):
            combi = "".join(perm)
            combi_byte = combi.encode()
            combi_hash = md5_hash(combi_byte)
            if combi_hash == hashed_psd:
                return combi
    return None