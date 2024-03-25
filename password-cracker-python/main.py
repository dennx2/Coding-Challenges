import logging
from utils.brute_force import brute_force
from utils.word_list import lookup_word_list
from utils.rainbow import lookup_rainbow_table

# print(md5(b'password')) # <md5 _hashlib.HASH object @ 0x0000013BB6603CB0>
# print(md5(b'password').hexdigest()) # 5f4dcc3b5aa765d61d8327deb882cf99

# logging.basicConfig(level=logging.DEBUG)

def main():
    hashed_psd = input("Enter the hash you want to crack: ")
    if not hashed_psd:
        hashed_psd = "2bdb742fc3d075ec6b73ea414f27819a"
    hashed_psd = hashed_psd.strip()

    method = input("Crack Method?\n(1) Brute force\n(2) Word list\n(3) Rainbow table\n")

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
                print("Invalid option, please try again.")
                exit()
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
