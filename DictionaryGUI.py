import requests
import json
from bs4 import BeautifulSoup
from difflib import get_close_matches
import re
import tkinter as tk


class Dictionary:
    def __init__(self):
        self.window = tk.Tk()
        self.window.minsize(200, 100)
        self.window["bg"] = "black"
        self.window.title("Kip Interactive Dictionary")
        self.label_space = tk.Label(self.window, bg="black")
        self.label_space.grid(row=0, column=0)
        self.label_initial = tk.Label(
            self.window,
            text="Input a word to define:",
            bg="black",
            fg="white")
        self.label_initial.config(font=("Courier", 15))
        self.label_initial.grid(row=1, column=0, columnspan=2)
        self.label_space = tk.Label(self.window, bg="black")
        self.label_space.grid(row=2, column=0)
        self.word_entry = tk.Entry(
            self.window,
            bg="black",
            fg="white")
        self.word_entry.grid(row=3, column=0)
        self.word_entry.config(font="Courier")
        self.submit_button = tk.Button(
            self.window,
            text="Submit",
            bg="#1dacd6",
            width=16,
            height=1,
            command=self.use_entry)
        self.submit_button.grid(row=3, column=1)
        self.submit_button.config(font="Courier")

    def use_entry(self):
        contents = self.word_entry.get()
        obj.main(contents)

    def display(self, definitions, number, title):
        obj.label_initial.grid_remove()
        obj.word_entry.grid_remove()
        obj.submit_button.grid_remove()
        try:
            self.button1.destroy()
            self.button2.destroy()
            self.label_check.destroy()
            self.label_space.destroy()

        except AttributeError:
            ...
        titler = tk.Label(text=title, bg="black", fg="white")
        titler.grid(row=0, column=0, sticky="W")
        titler.config(font=("Courier", 15))
        for i in range(number):
            definition = str(definitions[i]).capitalize()
            definit = tk.Label(
                text=(str(i+1)+": "+definition),
                bg="black",
                fg="white",
                wraplength=500)
            definit.grid(row=i+1, column=0, sticky="W")

    def displayfail(self, word):
        obj.match = word
        obj.label_initial.grid_remove()
        obj.word_entry.grid_remove()
        obj.submit_button.grid_remove()
        self.label_space = tk.Label(self.window, bg="black")
        self.label_space.grid(row=0, column=0)
        self.label_check = tk.Label(
            self.window,
            text='Did you mean "'+str(word)+'"?',
            bg="black",
            fg="white"
            )
        self.label_check.grid(row=1, column=0, columnspan=2)
        self.label_check.config(font="Courier")
        self.label_space = tk.Label(self.window, bg="black")
        self.label_space.grid(row=2, column=0)
        self.button1 = tk.Button(
            self.window,
            text="Yes",
            bg="#1dacd6",
            width=16,
            height=1,
            command=...)
        self.button1["command"] = lambda x=str(obj.match): self.main(str(x))
        self.button1.grid(row=3, column=0)
        self.button1.config(font="Courier")
        self.button2 = tk.Button(
            self.window,
            text="No",
            bg="#1dacd6",
            width=16,
            height=1,
            command=...)
        self.button2.grid(row=3, column=1)
        self.button2.config(font="Courier")

    def checker(self, soup, word, data):
        try:
            title = soup.find("span", {"class": "hw dhw"})
            title_text = title.text.title()

            definitions = []
            counter = 0
            for deff in soup.find_all("div", {"class": "def ddef_d db"}):
                deff = deff.text
                deff = re.sub(r":", "", deff)
                definitions.append(deff)
                counter += 1

            obj.display(definitions, counter, title_text)

        except AttributeError:
            obj.catcher(word, data)

    def catcher(self, word, data):
        if len(get_close_matches(word, data.keys())) > 0:
            match = get_close_matches(word, data.keys())[0]
            obj.displayfail(match)
        else:
            print("Sorry, we couldn't define that word. Please check for typos.")

    def main(self, word):
        r = requests.get(f"https://dictionary.cambridge.org/dictionary/english/{word.lower()}")
        c = r.text
        soup = BeautifulSoup(c, "html.parser")

        with open("dictionary.json") as dat:
            data = json.load(dat)
        obj.checker(soup, word, data)


obj = Dictionary()
obj.window.mainloop()
