# library imports
from bs4 import BeautifulSoup


def process_url(response):
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
