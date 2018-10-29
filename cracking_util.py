"""
This utils Create a master dictionary file with words padded to a length of 8
@author Aaron Harkrider
@date 10-29-18
"""

import argparse


def main():
    #  Parse in arguments from the cmd line
    parser = argparse.ArgumentParser(description="Create a master dictionary file with words padded to a length of 8")
    parser.add_argument("word_file", default="words", help="file of words, (defaults to words) ")
    parser.add_argument("-d", "--master_dictionary_file", metavar='', default="master_dictionary.txt",
                        help="Stores the words of length 8 or words of 5-7 padded to 8 (defaults to master_dictionary.txt)")
    parser.add_argument("-l", "--word_length_only", metavar='',
                        help="optional param to limit the words to only those of a particular length before padding.")

    args = parser.parse_args()

    # read in word_file

    print("Building a dictionary file from a word file.\n")

    master_dictionary = open(args.master_dictionary_file, "w+")  # creating a file if it doesn't exist

    with open(args.word_file) as word_file:

        for line in word_file:

            # if the word length is less then 8 add padding
            # NOTE: this could be improved but just doing this for now

            word = line.strip()
            if args.word_length_only:
                if len(word) != int(args.word_length_only):
                    continue

            if len(word) == 8:
                print("No padding needed for '{}'".format(word))
                master_dictionary.write(word + '\n')
            elif len(word) == 7:
                print("Adding 1 digit of padding to '{}'".format(word))
                for i in range(10):
                    # add the 0-9 as padding
                    master_dictionary.write(word + str(i) + '\n')
            elif len(word) == 6:
                print("Adding 2 digit of padding to '{}'".format(word))
                for i in range(10):
                    # add the 0-9 as padding
                    # e.g. spider0
                    padded_word1 = word + str(i)
                    for j in range(10):
                        # add the 0-9 as padding
                        # e.g spider00
                        # then spider01
                        # and so on
                        master_dictionary.write(padded_word1 + str(j) + '\n')
            elif len(word) == 5:
                print("Adding 3 digit of padding to '{}'".format(word))
                for i in range(10):
                    # add the 0-9 as padding
                    padded_word1 = word + str(i)
                    for j in range(10):
                        # add the 0-9 as padding
                        padded_word2 = padded_word1 + str(j)
                        for k in range(10):
                            # add the 0-9 as padding
                            master_dictionary.write(padded_word2 + str(k) + '\n')

    master_dictionary.close()


# Standard boilerplate to call the main function, if executed
if __name__ == '__main__':
    main()
