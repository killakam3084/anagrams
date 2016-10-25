# Tweet Anagram Finder
---
#### **anagrams/ contains:** 
- a file which parses input tweet data -- **anagrams.py**
- a file to make dummy tweet data given a dictionary -- **make_tweet.json**

#### **dictionaries/ contains:** 
- a small dictionary of the 1,000 most common words **common_word_dictionary.txt**
- a large dictionary of ~ 170,000 words -- **dictionary.txt**
- these are for passing to **make_tweet_json.py** to construct tweet data

#### **tweet_data/ contains:** 
- a small .json file of sample tweet data -- **tweets.json**

#### **bin/**
- the binaries to execute; added to path with `pip install`

#### _To execute_
1. **Clone repository:** `git clone https://github.com/killakam3084/anagrams.git`
2. **Install anagrams package** `cd anagrams/ && pip install .` 
3.  **Run script** 
		
		usage: find-anagrams [-h] input_file
				A vanilla program to detect anagrams in tweet json

		positional arguments:
		input_file  The input file of tweets.

		optional arguments:
		-h, --help  show this help message and exit

		Certainly this isn't how Anagramatron does it
4. _**Example**_
	`find-anagrams tweets.json`

#### *Notes on ijjson iterative parser***
- ijson is an iterative JSON parser with a standard Python iterator interface
- Ijson provides several implementations of the actual parsing in the form of backends located in ijson/backends:
- The script should output memory_profiler data showing the effectiveness of ijson's lazy loading
- Processed 50,000,000 two word tweets with words of length 4 in about ~ 2 hours, around ~3.5G file size.
