import PyPDF2
from nltk.corpus import stopwords

def tokenize(path):
    # open PDF
    pdf = PyPDF2.PdfFileReader(open(str(path),"rb"),strict = False)
    stopword_list = list(stopwords.words("english"))

    # read PDF file in a list
    pdf_content = []
    for page in pdf.pages:
        pdf_content.append(page.extractText())

    # tokenize all the words in file
    tokenize = []
    for line in pdf_content:
        tokenize = filter(None,(line.split(" ")))

    # remove punctuations and case-fold
    no_punctuations = []
    for token in tokenize:
        no_punctuations.append(token.rstrip(",:|.-").lower())

    # remove stop words
    without_stop_words = []

    for word in filter(None, no_punctuations):
        if word not in stopword_list:
            without_stop_words.append(word)

    return without_stop_words