import sys
import requests
import json
from bs4 import BeautifulSoup
from difflib import get_close_matches
import re


class Dictionary:

    def checker(self, soup, word, data):
        try:
            title = soup.find("span", {"class": "hw dhw"})
            print()
            print(title.text.title())
            print("\n")

            definitions = []
            counter = 0
            for deff in soup.find_all("div", {"class": "def ddef_d db"}):
                deff = deff.text
                deff = re.sub(r":", "", deff)
                definitions.append(deff)
                counter += 1

            for i in range(counter):
                definition = str(definitions[i]).capitalize().strip()
                print(f"{i + 1}: {definition}")
            sys.exit(0)

        except AttributeError:
            obj.catcher(word, data)

    def catcher(self, word, data):
        if len(get_close_matches(word, data.keys())) > 0:
            yn = input(f"Did you mean {get_close_matches(word, data.keys())[0]} instead? ")
            if yn[0].upper() == "Y":
                word = str(get_close_matches(word, data.keys())[0])
                r = requests.get(f"https://dictionary.cambridge.org/dictionary/english/{word.lower()}")
                c = r.text
                soup = BeautifulSoup(c, "html.parser")
                obj.checker(soup, word, data)
            elif yn[0].upper() == "N":
                print("Sorry, we couldn't define that word. Please check for typos.")
            else:
                print("Sorry, we didn't understand your entry.")
        else:
            print("Sorry, we couldn't define that word. Please check for typos.")

    def main(self):
        word = input("What word do you want to define?")

        r = requests.get(f"https://dictionary.cambridge.org/dictionary/english/{word.lower()}")
        c = r.text
        soup = BeautifulSoup(c, "html.parser")

        with open("dictionary.json") as dat:
            data = json.load(dat)
        obj.checker(soup, word, data)


obj = Dictionary()
obj.main()
