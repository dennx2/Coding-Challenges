import gzip
import logging

from .timer_decorator import timer
from .hash_function import md5_hash

# logging.basicConfig(level=logging.DEBUG)

@timer
def lookup_word_list(hashed_psd: str, word_list_path: str) -> str | None:
    """
    Look up a hashed password in a word list and return the corresponding plaintext password.
    """

    # Open the word list file using gzip
    with gzip.open(word_list_path, "rb") as f:
        for line in f:
            # Check if the hashed value matches the hashed password we are looking for
            psd = line.rstrip()
            if md5_hash(psd) != hashed_psd:
                continue
            # If match, try to decode the password from bytes to string
            try:
                return psd.decode()
            except UnicodeDecodeError as e:
                logging.error("Decoding failed", e)
                raise
        return None
