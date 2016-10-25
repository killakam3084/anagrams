#!/usr/bin/env python

import argparse
import ijson.backends.yajl2_cffi
import time
from memory_profiler import profile


class Tweet:
    """
    A representation of a Tweet
    """
    def __init__(self, tweet_id, original_tweet_text, tweet_text):

        self.id = tweet_id
        self.orig_text = original_tweet_text
        self.text = tweet_text


def permute_words(words):
    """
    Takes in a string of words and finds all of the permutations of
    the input words
    :param words: a space delimited string
    :return: either a set if there is more than one word to permute
             an empty set otherwise
    """

    words_list = words.split(' ')
    if len(words_list) > 1:
        used_list = [False for i in range(len(words_list))]
        res = ''
        res_set = set()
        permute(words_list, used_list, res, 0, res_set)
        return res_set
    else:
        return set()


def permute(words_list, used_list, res, level, res_list):
    """

    :param words_list: The list of word tokens
    :param used_list: Keeps track of which positions have been permuted
    :param res: the result string
    :param level: permuting each word through each possible position
    :param res_list: the resulting list of all permutations
    :return: recursive call
    """
    if level == len(words_list) and res:
        res_list.add(''.join(res.strip().split()))
        return
    for i in range(len(words_list)):
        if used_list[i]:
            continue
        else:
            used_list[i] = True
            permute(words_list, used_list, res + ' ' + words_list[i], level + 1,
                    res_list)
            used_list[i] = False


def parse_args():
    """
        Method to parse commandline argument of input file.

        :return: return nothing
    """
    global parser
    parser = argparse.ArgumentParser(
        description='A vanilla program to detect anagrams in tweet json',
        epilog='Certainly this isn\'t how Anagramatron does it')
    parser.add_argument('input_file',
                        type=argparse.FileType('r'),
                        help='The input file of tweets.'
                        )
    try:
        global args
        args = parser.parse_args()
    except IOError, msg:
        parser.error(str(msg))


@profile
def main():
    """
    Loads the input file iterates through it prints matching anagram tweets
    to std out
    :return: nothing
    """
    parse_args()
    global args
    tweet_id = ""
    tweet_text = ""

    with open(args.input_file.name, 'r') as input_file:
        parser = ijson.parse(input_file)

        tweet_obj_dict = {}
        print "Beginning to parse tweets in..."
        time_var = 5
        for i in range(time_var):
            print str(time_var)
            time.sleep(1)
            time_var -= 1

        for prefix, event, value in parser:
            if prefix == 'tweets.item.id':
                tweet_id = str(value)
            if prefix == 'tweets.item.text':
                original_text = str(value)
                tweet_text = "".join(original_text.split())
            if tweet_id and original_text:
                tweet_key = (''.join(
                    ch for ch in sorted(tweet_text.strip().lower()) if
                    ch.isalpha()))
                if tweet_key in tweet_obj_dict:
                    if tweet_text != tweet_obj_dict[tweet_key].text:
                        permutations = permute_words(
                            tweet_obj_dict[tweet_key].orig_text)
                        if tweet_text not in permutations:
                            print
                            print "*****ANAGRAMS FOUND!*****"
                            print "Original Tweet   id:{0} text:{1}".format(
                                tweet_obj_dict[tweet_key].id,
                                tweet_obj_dict[tweet_key].orig_text)
                            del tweet_obj_dict[tweet_key]
                            print "Anagram  Tweet   id:{0} text:{1}\n".format(
                                tweet_id, original_text)
                    else:
                        '''
                        print
                        print "*****DUPLICATE TWEETS FOUND!*****"
                        print "Original Tweet   id:{0} text:{1}".format(
                            tweet_obj_dict[tweet_key].id,
                            tweet_obj_dict[tweet_key].orig_text)
                        print "Duplicate  Tweet   id:{0} text:{1}\n".format(
                            tweet_id, original_text)
                            '''
                else:
                    tweet_obj = Tweet(tweet_id, original_text, tweet_text)
                    tweet_obj_dict[tweet_key] = tweet_obj
                print "Processed Tweet: " + "id:" + tweet_id + "    " + "text: " + original_text
                tweet_text = ""
                tweet_id = ""


if __name__ == '__main__':
    main()
