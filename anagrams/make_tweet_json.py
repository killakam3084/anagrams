#!/usr/local/env python
import json
import random
import argparse


def parse_args():
    """
        Method to parse commandline arguments of serving size and filter items

        :return: return nothing
    """
    global parser
    parser = argparse.ArgumentParser(
        description='A program to make dummy tweet json for anagrams'
    )
    parser.add_argument('output_file',
                        help='A output file to write tweet data to.'
                        )
    parser.add_argument('dictionary_file',
                        type=argparse.FileType('r'),
                        help='The dictionary to construct anagrams.'
                        )
    parser.add_argument('-l, word-length', type=int,
                        help='The max character count for a word.',
                        dest='word_length'
                        )
    parser.add_argument('-n, number-of-tweets', type=int,
                        help='The number of tweets to constructs.',
                        dest='num_tweets'
                        )
    try:
        global args
        args = parser.parse_args()
    except IOError, msg:
        parser.error(str(msg))


def make_word_string(word_list):
    """
    Constructs a string of text from the list of possible words constructed
    from the read in dictionary file
    :param word_list: The list of possible words
    :return: returns a leading and trailing striped string of text
    """
    word_str = ''
    for i in range(random.randint(1, args.word_length)):
        word_str += " " + word_list[random.randint(0, len(word_list) - 1)]
    return word_str.strip()


def generate_tweet_data():
    """
    Create the tweet json object and write it to file
    :return: return none
    """
    global args
    word_list = ([line.strip() for line in args.dictionary_file if
                  len(line.strip()) <= args.word_length])
    word_list.sort()
    tweet_obj = {
        'tweets': [{'id': str(i), 'text': make_word_string(word_list)} for i in
                   range(args.num_tweets)]}
    with open(args.output_file, 'w') as outfile:
        json.dump(tweet_obj, outfile, indent=4)


def main():
    parse_args()
    generate_tweet_data()


if __name__ == '__main__':
    main()
