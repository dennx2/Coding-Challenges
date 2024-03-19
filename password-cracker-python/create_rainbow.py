import gzip
from hashlib import md5
import logging

logging.basicConfig(level=logging.DEBUG)


def create_rainbow_table(word_list_path: str, rainbow_path: str) -> None:
    """
    Create a rainbow table file with a word list
    """
    with gzip.open(word_list_path, "rb") as input:
        with gzip.open(rainbow_path, "wb") as output:
            for psd in input.readlines():
                content = f"{md5(psd.strip()).hexdigest()}|delimiter|"
                # logging.debug(content)
                output.write(content.encode() + psd)


if __name__ == "__main__":
    create_rainbow_table("src/crackstation-human-only.txt.gz", "src/rainbow-table.gz")
