import pdfplumber
from typing import List, Dict
from datetime import date


class TextualWord:
    def __init__(self, x0: float, x1: float, text: str):
        self.x0 = x0
        self.x1 = x1
        self.text = text


PagesToWords = Dict[int, List[TextualWord]]


class Chart:
    def __init__(self, name: str, dob: date, has_valid_ekg: bool):
        self.name = name
        self.dob = dob
        self.has_valid_ekg = has_valid_ekg

    @property
    def age(self) -> float:
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age


def populate_chart(page_to_words: PagesToWords) -> Chart:
    name = ""
    dob = None
    has_valid_ekg = False

    for page_number, words in page_to_words.items():
        mame_flag = False
        for word in words:
            if word.text == "DOB:":
                mame_flag = False
                dob_text = words[words.index(word) + 1].text  # Get the word after "Dob:"
                dob = date(*map(int, dob_text.split("/")[::-1]))
            if word.text == "EKG":
                has_valid_ekg = words[words.index(word) + 2].text.lower() == "valid"
            if mame_flag:
                name += words[words.index(word)].text + " "  # Get the word after "Name:"
            if word.text == "Name:":
                mame_flag = True

    return Chart(name, dob, has_valid_ekg)


def pdf_to_dict(pdfplumber_pdf: pdfplumber.PDF) -> PagesToWords:
    pages_to_words = {}  # Initialize an empty dictionary to store the result

    for page_number in range(len(pdfplumber_pdf.pages)):
        page = pdfplumber_pdf.pages[page_number]
        words = [TextualWord(word['x0'], word['x1'], word['text']) for word in page.extract_words()]
        pages_to_words[page_number + 1] = words  # Page numbers start from 1

    return pages_to_words


def print_chart(chart: Chart):
    print(f"age: {chart.age}")
    for key, value in vars(chart).items():
        print(f"{key}: {value}")


class ExtraTextualWord(TextualWord):
    def __init__(self, x0: float, x1: float, text: str, fontname: str, size: float):
        super().__init__(x0, x1, text)
        self.fontname = fontname
        self.size = size

    @property
    def is_bold(self) -> bool:
        return 'Bold' in self.fontname


PagesToExtraWords = Dict[int, List[ExtraTextualWord]]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 1
    pdf_path = "/home/tehila/Downloads/chart_example.pdf"

    with pdfplumber.open(pdf_path) as pdf:
        result = pdf_to_dict(pdf)
        for page_number, words in result.items():
            print(f"{page_number}:")
            for word in words:
                print(f"  {word.text}, x0: {word.x0}, x1: {word.x1}")

    # 2
    pdf_path = "/home/tehila/Downloads/chart3.pdf"

    with pdfplumber.open(pdf_path) as pdf:
        result = pdf_to_dict(pdf)
        chart = populate_chart(result)
        print_chart(chart)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
