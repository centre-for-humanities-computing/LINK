# import the llp module
import llp
# import regular expressions
import re
# import sys for command line arguments
import sys, getopt

# imports for making histograms
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import random
from collections import Counter


# load the ECCO-TCP corpus
corpus = llp.load('ECCO_TCP')

# Get a text
texts = corpus.texts()
textNumber = sys.argv[1]
textTitle = "Text no. " + textNumber
text = texts[int(textNumber)]

# Get the metadata as a dictionary
metadata = text.meta

# Get the plain text as a string
txt = text.txt


# The text is given in one long string, but we are interested in words pr. sentence
# therefor we start by dividing the text into sentencesself.

# Dots that must be ignored in sentence-split.
# E.g. we do not encounter a new sentence after the dot in: "Mrs. Campbell ..."
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

# Method for splitting the text into to sentences.
def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

# Array containing all the sentences in the text
sentenceArray = split_into_sentences(txt)
valuesList = []

# Now we can count the number of words in each sentence
for index in range(len(sentenceArray)):
    # using regex to count words in string
    res = len(re.findall(r'\w+', sentenceArray[index]))
    # adding the result to the list
    valuesList.append(res)


# getting the frequencies of the sentence length
counted = Counter(valuesList)

# plotting a histogram for sentence length
plt.bar(list(counted.keys()), counted.values(), color='g')

# Setting the title to be the text number and amount of sentences in the text
pltTitle = textTitle + ", contains " + str(len(sentenceArray)) + " sentences"
plt.title(pltTitle)
plt.xlabel('Value: Sentence Length')
plt.ylabel('Frequency')
plt.show()
