# library imports
import json
from difflib import get_close_matches


def get_matches(word):

	# open and load a dictionary
	with open("dictionary.json") as dictionary:
		data = json.load(dictionary)

	# get similar words
	matches = get_close_matches(word, data.keys())
	return matches[0] if matches else ""
