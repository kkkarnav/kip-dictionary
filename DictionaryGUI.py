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
        self.window.resizable(width=False, height=False)
        self.window["bg"] = "#222021"
        self.window.title("Kip Interactive Dictionary")
        self.restart_button = tk.Button(
            self.window,
            text="Restart",
            bg="#008ecc",
            fg="Black",
            width=10,
            height=1,
            relief="flat",
            command=lambda: [self.window.destroy(), self.__init__()]
        )
        self.restart_button.config(font="Courier")
        self.window.bind("<Shift-Escape>", lambda x: [self.window.destroy(), self.window.mainloop()])
        self.restart_button.grid(row=0, column=3)
        self.quit_button = tk.Button(
            self.window,
            text="Quit",
            bg="#008ecc",
            fg="Black",
            width=10,
            height=1,
            relief="flat",
            command=lambda: self.window.destroy()
        )
        self.quit_button.config(font="Courier")
        self.window.bind("<Escape>", lambda x: self.window.grid_remove())
        self.quit_button.grid(row=1, column=3)
        self.label_space = tk.Label(self.window, bg="#222021")
        self.label_space.grid(row=0, column=0)
        self.label_space.grid(row=1, column=0)
        self.label_space.grid(row=2, column=0)
        self.label_initial = tk.Label(
            self.window,
            text="Input a word to define:",
            bg="#222021",
            fg="white",)
        self.label_initial.config(font=("Courier", 15))
        self.label_initial.grid(row=2, column=0, columnspan=3)
        self.label_space = tk.Label(self.window, bg="#222021")
        self.label_space.grid(row=3, column=0)
        self.word_entry = tk.Entry(
            self.window,
            bg="#0f0f0f",
            fg="white",
            insertbackground="#008ecc",
            relief="flat")
        self.word_entry.config(font="Courier")
        self.word_entry.focus()
        self.word_entry.grid(row=4, column=0)
        self.submit_button = tk.Button(
            self.window,
            text="Submit",
            bg="#008ecc",
            width=16,
            height=1,
            relief="flat",
            command=self.use_entry)
        self.submit_button.config(font="Courier")
        self.submit_button.grid(row=4, column=2)
        self.window.bind("<Return>", lambda x: self.use_entry())
        self.button1 = tk.Button(
            self.window,
            text="Yes",
            bg="#008ecc",
            width=16,
            height=1,
            relief="flat",
            command=...)
        self.button2 = tk.Button(
            self.window,
            text="No",
            bg="#008ecc",
            width=16,
            height=1,
            relief="flat",
            command=...)
        self.label_end = tk.Label(
            self.window,
            text="Sorry, we couldn't define that word. \nPlease check for typos.",
            bg="#222021",
            fg="white")
        self.label_end.config(font=("Courier", 15))

    def use_entry(self):
        contents = self.word_entry.get()
        self.main(contents)

    def display(self, definitions, number, title, src):
        try:
            self.button1.grid_remove()
            self.button2.grid_remove()
            self.label_check.grid_remove()
            self.label_space.grid_remove()

        except:
            ...

        self.label_initial.grid_remove()
        self.word_entry.grid_remove()
        self.submit_button.grid_remove()

        titler = tk.Label(text=title, bg="#222021", fg="white")
        titler.grid(row=1, column=0, sticky="W")
        titler.config(font=("Courier", 15))
        for i in range(number):
            definition = str(definitions[i]).capitalize()
            definit = tk.Label(
                text=(definition if src == "Wiki"
                      else (str(i+1)+": "+str(definition))),
                bg="#222021",
                fg="white",
                wraplength=500)
            definit.grid(row=i+2, column=0, sticky="W")

    def displayfail(self, words):
        for word in reversed(words):
            try:
                self.button1.grid_remove()
                self.button2.grid_remove()
                self.label_check.grid_remove()
                self.label_space.grid_remove()
            except:
                ...

            try:
                self.label_initial.grid_remove()
                self.word_entry.grid_remove()
                self.submit_button.grid_remove()
            except:
                ...

            self.label_space = tk.Label(self.window, bg="#222021")
            self.label_space.grid(row=0, column=0)
            self.label_check = tk.Label(
                self.window,
                text='Did you mean "' + str(word) + '"?',
                bg="#222021",
                fg="white"
            )
            self.label_check.grid(row=1, column=0, columnspan=2)
            self.label_check.config(font="Courier")
            self.label_space.grid(row=2, column=0)

            self.button1["command"] = lambda x=str(word): [self.main(str(x))]
            self.button1.grid(row=3, column=0)
            self.button1.config(font="Courier")

            self.button2["command"] = lambda x=words: [self.no_button(x)]
            self.button2.grid(row=3, column=1)
            self.button2.config(font="Courier")

    def no_button(self, words):
        words = [i for i in words[1:]]
        if not words:
            self.end_screen()
        self.displayfail(words)

    def end_screen(self):
        self.button1.grid_remove()
        self.button2.grid_remove()
        self.label_check.grid_remove()
        self.label_space.grid_remove()

        self.button1.grid_remove()
        self.button2.grid_remove()
        self.label_check.grid_remove()
        self.label_space.grid_remove()

        self.label_end.grid(row=1, column=0, columnspan=2)

    def checker(self, soup, word, data, source):
        if source == "Urban":
            try:
                title = soup.find("a", {"class": "word"})
                title_text = title.text.title()

                definitions = []
                counter = 0
                for deff in soup.find_all("div", {"class": "meaning"}):
                    deff = deff.text
                    definitions.append(deff)
                    counter += 1
                    if counter >= 3:
                        break

                self.display(definitions, counter, title_text, source)

            except AttributeError:
                self.catcher(word, data)

        elif source == "Wiki":
            try:
                title = soup.find("h1", {"class": "firstHeading"})
                title_text = title.text
                title_text = title_text.title()

                definitions = []
                counter = 0
                for deff in soup.find_all("ol"):
                    deff = deff.text.upper()
                    definitions.append(str(counter+1)+": "+str(deff))
                    counter += 1
                    if counter >= 3:
                        break

                success = False
                try:
                    definitions[0]

                except IndexError:
                    success = True

                if success:
                    self.catcher(word, data)
                else:
                    self.display(definitions, counter, title_text, source)

            except AttributeError:
                self.catcher(word, data)

        elif source == "Default":
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

                self.display(definitions, counter, title_text, source)

            except AttributeError:
                self.catcher(word, data)

    def catcher(self, word, data):
        if len(get_close_matches(word, data.keys())) > 0:
            match = get_close_matches(word, data.keys())
            self.displayfail(match)
        else:
            self.end_screen()

    def main(self, word):
        r = requests.get(f"https://dictionary.cambridge.org/dictionary/english/{word.lower()}")
        c = r.text
        soup = BeautifulSoup(c, "html.parser")

        src = "Default"

        try:
            title = soup.find("span", {"class": "hw dhw"})
            title.text.title()
            if title.text.lower() != word.lower():
                src = "Wiki"

        except AttributeError:
            src = "Wiki"

        if src == "Wiki":
            word2 = word.replace(" ", "_")
            r = requests.get(f"https://en.wiktionary.org/wiki/{word2.strip().lower()}")
            c = r.text
            soup = BeautifulSoup(c, "html.parser")
            try:
                title = soup.find("ol")
                title.text.title()

            except AttributeError:
                src = "Urban"
                r = requests.get(f"https://www.urbandictionary.com/define.php?term={word.lower()}")
                c = r.text
                soup = BeautifulSoup(c, "html.parser")

        with open("dictionary.json") as dat:
            data = json.load(dat)
        self.checker(soup, word, data, src)


if __name__ == "__main__":
    obj = Dictionary()
    obj.window.mainloop()
