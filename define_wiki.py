# library imports
from bs4 import BeautifulSoup


def process_url(response):
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
