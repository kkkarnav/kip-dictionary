# imports
import requests
from bs4 import BeautifulSoup
import random


# scrape the accepted url and return the response
def get_result(url):
	return requests.get((url + word.strip().lower()), headers=header[random.randrange(0, 5)])


# check if the accepted response from the accepted source is a success or failure
def check_result(returned_response, source):
	if returned_response.status_code == 404:
		print('_________________________________________________')
		print('No result found in ' + source)
	elif returned_response.status_code == 200:
		print('_________________________________________________')
		print('Result found in ' + source)
	else:
		print('_________________________________________________')
		print('Unable to reach' + source)
	return returned_response


def process_url_wiki(response):
	soup = BeautifulSoup(response.text, 'html.parser')

	# finds the title and definitions on the definition page
	output_lines = soup.find_all('ol')

	# print the title
	title = soup.find(True, class_=['firstHeading'])
	print(title.text.title(), '\n')

	# iterate on each returned list of definitions
	for output_count, output in enumerate(output_lines):
		# iterate on each returned definition
		for content_count, content in enumerate(output):
			# proceed if the definition is a valid tag
			if str(type(content)) == "<class 'bs4.element.Tag'>":
				content_text = content.text
				content_text = '> ' + content_text + '\n'
				print(content_text)


def process_url_urban(response):
	soup = BeautifulSoup(response.text, 'html.parser')

	# finds the first title and definition on the definition page
	output = soup.find(True, class_=['meaning'])
	title = soup.find(True, class_=['word'])

	# print the title
	print(title.text.title())

	# print the definition
	output_text = output.text
	print('> ' + output_text)

	# block to handle a list of definitions with <br>s
	# for output_text in output.childGenerator():
	#   if str(type(output_text)) == "<class 'bs4.element.NavigableString'>":
	#        print('> ' + str(output_text))


def process_url_cambridge(response):
	soup = BeautifulSoup(response.text, 'html.parser')

	# finds the title, sub-titles, and definitions on the definition page
	output_lines = soup.find_all(True, class_=['hw dhw', 'phrase-title', 'def ddef_d db'])
	titles = soup.find_all(True, class_=['hw dhw'])
	phrase_titles = soup.find_all(True, class_=['phrase-title'])

	# iterates on each returned text
	for output_count, output in enumerate(output_lines):
		output_text = output.text

		# remove colons from end of definitions
		if output_text[-2] == ':':
			output_text = output_text[:-2]
		# avoid repetition of the main definition title
		if output in titles and output_count != 0:
			continue
		# small formatting for definition titles
		if output in phrase_titles:
			output_text = '\n' + output_text
		# bullet the definitions
		if output not in titles and output not in phrase_titles:
			output_text = '> ' + output_text

		print(output_text)


if __name__ == '__main__':

	# accepting input word from the user
	word = input('What word do you want to define?')

	# defining the headers to use and the urls to scrape
	header = [{'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'},
			{'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'},
			{'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'},
			{'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'},
			{'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}]
	url_wiki = 'https://en.wiktionary.org/wiki/'
	url_urban = 'https://www.urbandictionary.com/define.php?term='
	url_cambridge = 'https://dictionary.cambridge.org/dictionary/english/'

	# get the definitions from the three sites
	process_url_cambridge(check_result(get_result(url_cambridge), 'cambridge dictionary'))
	process_url_wiki(check_result(get_result(url_wiki), 'wiktionary'))
	try:
		process_url_urban(check_result(get_result(url_urban), 'urban dictionary'))
	except AttributeError:
		print('An error was occurred while looking in urban dictionary')
