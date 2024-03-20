from hashlib import md5
import string
from itertools import permutations
import gzip
import logging

# print(md5(b'password')) # <md5 _hashlib.HASH object @ 0x0000013BB6603CB0>
# print(md5(b'password').hexdigest()) # 5f4dcc3b5aa765d61d8327deb882cf99

logging.basicConfig(level=logging.DEBUG)


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


def main():
    hashed_psd = input("Enter the hash you want to crack: ")
    method = input("Crack Method?\n(1) Brute force\n(2) Word list\n(3) Rainbow table\n")
    hashed_psd = hashed_psd.strip()

    try:
        match method:
            case "1":
                print("Cracking...")
                result = brute_force(hashed_psd)
            case "2":
                word_list_path = input("Provide the path to the word list: ")
                if not word_list_path:
                    word_list_path = "src/crackstation-human-only.txt.gz"

                print("Cracking...")
                result = lookup_word_list(hashed_psd, word_list_path)
            case "3":
                rainbow_path = input("Provide the path to the rainbow table: ")
                if not rainbow_path:
                    rainbow_path = "src/rainbow-table.gz"

                print("Cracking...")
                result = lookup_rainbow_table(hashed_psd, rainbow_path)
            case _:
                pass
    except Exception as e:
        logging.error("Something went wrong:", e)
    else:
        if result:
            print("Match found!")
            print(result)
        else:
            print("No match was found.")


if __name__ == "__main__":
    main()

    # 2bdb742fc3d075ec6b73ea414f27819a
