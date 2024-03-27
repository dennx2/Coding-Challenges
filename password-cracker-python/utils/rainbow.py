import gzip
import logging

from .timer_decorator import timer
from .hash_function import md5_hash

logging.basicConfig(level=logging.DEBUG)

@timer
def create_rainbow_table(word_list_path: str, rainbow_path: str) -> None:
    """
    Create a rainbow table file with a word list
    """

    # Open the word list file for reading and the rainbow table file for writing
    with gzip.open(word_list_path, "rb") as input, gzip.open(rainbow_path, "wb") as output:
        bulk = []
        BATCH_SIZE = 1000
        delimiter = "|delimiter|"
        for psd in input:
            # Calculate the hash of the password and format it with a delimiter
            hashed_psd = md5_hash(psd.strip())
            content = f"{hashed_psd}{delimiter}"
            try:
                # Encode the content to bytes
                b_content = content.encode()
            except UnicodeEncodeError as e:
                logging.error("Encoding failed:", e)
                raise
            
            bulk.append(b_content + psd)
            
            # Write the content and the original password to the rainbow table in bytes
            if len(bulk) > BATCH_SIZE:
                output.writelines(bulk)
                bulk.clear()


def process_line(line: bytes, b_hashed_psd: bytes):
    line = line.rstrip()
    hashed, psd = line.split(b"|delimiter|")

    # Check if the hashed value matches the hashed password we are looking for
    if hashed != b_hashed_psd:
        return None
    
    # If match, try to decode the password from bytes to string
    try:
        return psd.decode()
    except UnicodeDecodeError as e:
        logging.error("Decoding failed", e)
        raise

        


@timer
def lookup_rainbow_table(hashed_psd: str, rainbow_path: str) -> str | None:
    """
    Look up a hashed password in a rainbow table and return the corresponding plaintext password.
    """

    # Open the rainbow table file using gzip
    with gzip.open(rainbow_path, "rb") as f:
        # Convert the hashed password into bytes
        b_hashed_psd = hashed_psd.strip().encode()

        for line in f:
            result = process_line(line, b_hashed_psd)
            if result is not None:
                return result

        return None


if __name__ == "__main__":
    create_rainbow_table("src/crackstation-human-only.txt.gz", "src/rainbow-table.gz")
