"""
@author Aaron Harkrider
@date 10-29-18

version 3.0.0
    * reduced clutter
    * improved runtime
    * default argparse params
"""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import argparse
import time


def main():
    print("Starting Aaron's password cracking program.\n")

    #  Parse in arguments from the cmd line
    parser = argparse.ArgumentParser()
    parser.add_argument("cracked_digests", default="cracked_digests.csv",
                        help="stores the digests found with matched password (defaults to cracked_digests.csv)")
    parser.add_argument('-p', '--passwords_file', default=".awharkrider_digests.csv",
                        help="password file of .csv (defaults to .awharkrider_digests.csv)")
    parser.add_argument('-d', "--dictionary_file", default="master_dictionary.txt",
                        help="dictionary file, (defaults to master_dictionary.txt) ")

    args = parser.parse_args()

    print("Reading in digests")
    # Read in passwords description file
    salty_digests = []
    with open(args.passwords_file) as passwords:
        for line in passwords:
            salty_digests.append(line)

    found_passwords = []
    with open(args.cracked_digests, 'r') as found_file:

        # remove found digest from the digest array
        print("...Improving search time by removing already cracked digests.\n")
        for line in found_file:
            found_salt, found_digest, found_password = line.strip().split(',')

            # saving found passwords so we can skip words in our dictionary if we already cracked them
            found_passwords.append(found_password)

            found_salty_digest = found_salt + ',' + found_digest + '\n'  # building line that matches the digest file
            if found_salty_digest in salty_digests:
                salty_digests.remove(found_salty_digest)

    found_file.close()

    print("Starting password brute force search!\n")
    then = time.time()  # Time before the operations start

    # read in dictionary_file
    with open(args.dictionary_file) as dict_file:
        for line in dict_file:
            word = line.strip()
            if word in found_passwords:
                # Word already cracked moving on
                continue

            # attempting to crack
            for digest_line in salty_digests:

                salt, digest = digest_line.strip().split(',')

                backend = default_backend()

                # Salts should be randomly generated
                salt_bytes = bytes.fromhex(salt)

                # derive
                kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                                 length=32,
                                 salt=salt_bytes,
                                 iterations=100000,
                                 backend=backend)

                key = kdf.derive(word.encode('utf-8'))

                digest_bytes = bytes.fromhex(digest)

                # check if we found a match
                if key == digest_bytes:
                    print('FOUND digest for {}.\n'.format(word))
                    print('digest: {},\n digest_bytes: {},\n word: {}\n'.format(digest, digest_bytes, word))
                    cracked = salt + ',' + digest

                    with open(args.cracked_digests, 'a+') as cracked_file:
                        cracked_file.write(cracked + ',' + word + '\n')

                    # removing the cracked digest from search space
                    salty_digests.remove(cracked + '\n')

    now = time.time()  # Time after it finished
    print("It took: ", now - then, " seconds to iterate through the entire dictionary and digests.\n")


# Standard boilerplate to call the main function, if executed
if __name__ == '__main__':
    main()
