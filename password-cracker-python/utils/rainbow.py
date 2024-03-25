import gzip
from hashlib import md5
import logging

# logging.basicConfig(level=logging.DEBUG)


def create_rainbow_table(word_list_path: str, rainbow_path: str) -> None:
    """
    Create a rainbow table file with a word list
    """

    # Open the word list file for reading and the rainbow table file for writing
    with gzip.open(word_list_path, "rb") as input:
        with gzip.open(rainbow_path, "wb") as output:
            for psd in input.readlines():
                # Calculate the hash of the password and format it with a delimiter
                delimiter = "|delimiter|"
                content = f"{md5(psd.strip()).hexdigest()}{delimiter}"
                try:
                    # Encode the content to bytes
                    b_content = content.encode()
                except UnicodeEncodeError as e:
                    logging.error("Encoding failed:", e)
                else:
                    # Write the content and the original password to the rainbow table in bytes
                    output.write(b_content + psd)


def lookup_rainbow_table(hashed_psd: str, rainbow_path: str) -> str | None:
    """
    Look up a hashed password in a rainbow table and return the corresponding plaintext password.
    """

    # Open the rainbow table file using gzip
    with gzip.open(rainbow_path, "rb") as f:
        # Convert the hashed password into bytes
        b_hashed_psd = hashed_psd.strip().encode()

        for line in f.readlines():
            line = line.rstrip()
            hashed, psd = line.split(b"|delimiter|")

            # Check if the hashed value matches the hashed password we are looking for
            if hashed != b_hashed_psd:
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


if __name__ == "__main__":
    create_rainbow_table("src/crackstation-human-only.txt.gz", "src/rainbow-table.gz")
