import gzip
from hashlib import md5
import logging

# logging.basicConfig(level=logging.DEBUG)

def lookup_word_list(hashed_psd: str, word_list_path: str) -> str | None:
    """
    Look up a hashed password in a word list and return the corresponding plaintext password.
    """

    # Open the word list file using gzip
    with gzip.open(word_list_path, "rb") as f:
        for psd in f.readlines():

            # Check if the hashed value matches the hashed password we are looking for
            if md5(psd.strip()).hexdigest() != hashed_psd:
                continue

            # If match, try to decode the password from bytes to string
            try:
                u_psd = psd.decode()
            except UnicodeDecodeError as e:
                logging.error("Decoding failed")
                raise
            else:
                return u_psd

        return None