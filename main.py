# module imports
from web_scraper import Scraper
import define_cambridge
import define_wiki
import define_urban
import define_local
import similar_words

# TODO: fix wiktionary and urban dict returning nothing


# add the definition from each source to the result list
def grab_definitions(url_sources, word):

	url_results = []

	# scrape each url source and add the result to the list
	for url_source in url_sources:

		# scrape the url for the word
		returned_page = scraper.scrape(url_source[1], word)

		# special case for cambridge dict redirecting without returning 404
		if "<title>Cambridge English Dictionary: Meanings &amp; Definitions</title>" in returned_page.text:
			continue

		# add found definitions to hits
		if returned_page.status_code == 200:
			url_results.append([url_source[0], returned_page])

	# parse the local source and add the result to the list
	local_result = define_local.grab_definition(word)
	if local_result:
		url_results.append(["local", local_result])

	return url_results


# go through similar words if no definitions are found
def handle_missing_output(url_sources, word):
	print(f'Sorry, no definitions were found for "{word}".')

	# check if a similar word exists
	similar_word = similar_words.get_matches(word)

	if similar_word:

		user_choice = input(f'Did you mean "{similar_word}"? <yes> ')

		# define the similar word if the user meant it
		if not user_choice or user_choice[0] == "y":

			# recursively call grab_definitions()
			grab_definitions(url_sources, similar_word)
			return

		else:
			print("Sorry, no other similar words were found.")
	else:
		print("Sorry, no similar words were found either.")


# print the definitions from the sources the user picks
def handle_output(url_results):

	cambridge_printed = False
	to_print = {}

	# display cambridge definition by default if found
	if url_results[0][0] == "cambridge dictionary":
		define_cambridge.process_url(url_results[0][1])
		url_results = url_results[1:]
		cambridge_printed = True

	# print a menu of definition sources
	print("Pick another definition: " if cambridge_printed else "Pick a definition")
	for result_index, result in enumerate(url_results):
		print(f"{result[0]} <{result_index + 1}>")
		to_print[result_index+1] = result[0]

	user_choice = int(input())

	# handle user choice of definition source
	if to_print[user_choice] == "wiktionary":
		define_wiki.process_url(url_results[user_choice-1][1])
	elif to_print[user_choice] == "urban dictionary":
		define_urban.process_url(url_results[user_choice-1][1])
	elif to_print[user_choice] == "local":
		for print_item in url_results[user_choice-1][1]:
			print(print_item)
	else:
		print("Sorry, couldn't find another definition.")


if __name__ == '__main__':

	scraper = Scraper()

	# accepting input word from the user
	input_word = input('What word do you want to define?')

	# define the urls to scrape
	urls = [["cambridge dictionary", 'https://dictionary.cambridge.org/dictionary/english/'],
			["wiktionary", 'https://en.wiktionary.org/wiki/'],
			["urban dictionary", 'https://www.urbandictionary.com/define.php?term=']]

	# get and handle returned definitions
	if not grab_definitions(urls, input_word):
		handle_missing_output(urls, input_word)
	else:
		handle_output(grab_definitions(urls, input_word))
