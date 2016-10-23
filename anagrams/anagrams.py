from memory_profiler import profile
from tweet import Tweet
import os
import ijson
import argparse

MIN_WORD_SIZE = 2  # min size of a word in the output


# Tries are crazy cool. Many thanks to Foglebird on S.O.
class Node(object):
    def __init__(self, letter='', final=False, depth=0):
        self.letter = letter
        self.final = final
        self.depth = depth
        self.children = {}

    def add(self, letters):
        node = self
        for index, letter in enumerate(letters):
            if letter not in node.children:
                node.children[letter] = Node(letter, index == len(letters) - 1,
                                             index + 1)
            node = node.children[letter]

    def anagram(self, letters):
        tiles = {}
        for letter in letters:
            tiles[letter] = tiles.get(letter, 0) + 1
        min_length = len(letters)
        return self._anagram(tiles, [], self, min_length)

    def _anagram(self, tiles, path, root, min_length):
        if self.final and self.depth >= MIN_WORD_SIZE:
            word = ''.join(path)
            length = len(word.replace(' ', ''))
            if length >= min_length:
                yield word
            path.append(' ')
            for word in root._anagram(tiles, path, root, min_length):
                yield word
            path.pop()
        for letter, node in self.children.iteritems():
            count = tiles.get(letter, 0)
            if count == 0:
                continue
            tiles[letter] = count - 1
            path.append(letter)
            for word in node._anagram(tiles, path, root, min_length):
                yield word
            path.pop()
            tiles[letter] = count


def parse_args():
    """
        Method to parse commandline arguments of serving size and filter items

        :return: return nothing
    """
    global parser
    parser = argparse.ArgumentParser(
        description='A vanilla program to detect anagrams in tweet json',
        epilog='Certainly this isn\'t how Anagramatron does it')
    parser.add_argument('input_file',
                        type=argparse.FileType('rt'),
                        help='The input file of tweets.'
                        )
    parser.add_argument('dictionary_file',
                        type=argparse.FileType('rt'),
                        help='The dictionary to construct anagrams.'
                        )
    try:
        global args
        args = parser.parse_args()
    except IOError, msg:
        parser.error(str(msg))


def load_dictionary(f):
    result = Node()
    for line in f:
        word = line.strip().lower()
        result.add(word)
    return result


# @profile
def main():
    parse_args()

    global args
    dict_fn = args.dictionary_file
    print 'Loading word list.\n'
    words = load_dictionary(dict_fn)

    input_file = args.input_file
    tweet_obj_dict = {}
    parser = ijson.parse(input_file)
    tweet_id = ""
    tweet_text = ""
    for prefix, event, value in parser:
        if prefix == 'tweets.item.id':
            tweet_id = str(value)
        elif prefix == 'tweets.item.text':
            tweet_text = str(value)

        if tweet_id and tweet_text and tweet_text not in tweet_obj_dict:
            for t, tweet_obj in tweet_obj_dict.iteritems():
                if tweet_text in tweet_obj.anagram_set:
                    print "Original Tweet:::::id:{0} text:\"{1}\"".format(
                        tweet_obj.id,
                        tweet_obj.text)
                    print "Anagram  Tweet:::::id:{0} text:\"{1}\"\n".format(
                        tweet_id, tweet_text)

                break
            tweet_text = ''.join(
                ch for ch in tweet_text.strip().lower() if
                ch.isalpha())
            if not tweet_text:
                break
            tweet_set = set()
            for word in words.anagram(tweet_text):
                tweet_set.add(word)
            tweet_obj = Tweet(tweet_id, tweet_text, tweet_set)
            tweet_obj_dict[tweet_text] = tweet_obj
            tweet_text = ""
            tweet_id = ""


if __name__ == '__main__':
    main()
