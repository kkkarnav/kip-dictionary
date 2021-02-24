# library imports
import json


def grab_definition(word):

	# open and load the local dictionary
	with open("dictionary.json") as dictionary:
		data = json.load(dictionary)

	definition = ""
	if word in data.keys():
		definition = data[word]

	return definition
