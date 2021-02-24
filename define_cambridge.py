# library imports
from bs4 import BeautifulSoup


def process_url(response):
	print(response)
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
