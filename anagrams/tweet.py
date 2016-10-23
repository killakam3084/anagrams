from collections import defaultdict

__author__ = 'vzfg38'


class Tweet:

    def __init__(self, tweet_id, tweet_text, anagram_set):
        self.id = tweet_id
        self.text = tweet_text
        self.anagram_set = anagram_set

