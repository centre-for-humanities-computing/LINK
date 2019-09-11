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
import matplotlib.lines as mlines
from collections import Counter

# The file with the stop words
file = open('stopwords.txt','r')
# .lower() returns a version with all upper case characters replaced with lower case characters.
text = file.read().lower()
file.close()
# replaces anything that is not a lowercase letter, a space, or an apostrophe with a space:
stopwords = re.sub('[^a-z\ \']+', " ", text)
stopwordsList = list(stopwords.split())


# load the ECCO-TCP corpus
corpus = llp.load('ECCO_TCP')
# Loads the texts from the ECCO corpus
texts = corpus.texts()

# getting the first text
textNumber1 = sys.argv[1]
textTitle1 = "Text no. " + textNumber1
text1 = texts[int(textNumber1)]

# getting the second text
textNumber2 = sys.argv[2]
textTitle2 = "Text no. " + textNumber2
text2 = texts[int(textNumber2)]

# Get the plain texts as a strings
txt1 = text1.txt
txt2 = text2.txt

# Find the total number of words in the text
numberOfWordsFirstText = len(re.findall(r'\w+', txt1))
numberOfWordsSecondText = len(re.findall(r'\w+', txt2))

def build_word_stop_dictionary(text):
    wordList = []
    # For all words in the text we check if it is on the 'stopwordlist'
    for word in text.split():
        if word in stopwordsList:
            # and if it is, we add it to the list of words for each text:
            wordList.append(word)
    # getting the frequencies of the words
    # this gives us dictionaries saying how many times the stopwords are encountered in the text
    return Counter(wordList)

countedWordsInText1 = build_word_stop_dictionary(txt1)
countedWordsInText2 = build_word_stop_dictionary(txt2)


# For the Scatter plot we want the first text on the x-axis, the second text on the y-axis, and the words as dot-labels
label = []
x = []
y = []
for key in countedWordsInText1:
    # we are only looking at stopwords which are encountered in both texts
    if key in countedWordsInText2:
        label.append(key)
        # Here we normalize the number of word observations compared to the total amount of words in the text
        x_value = (countedWordsInText1.get(key) / numberOfWordsFirstText) * 100
        x.append(x_value)
        y_value  = (countedWordsInText2.get(key) / numberOfWordsSecondText) * 100
        y.append(y_value)

# Making a scatter plot of size 8x8
fig, ax = plt.subplots(figsize=(8,8))
ax.scatter(x, y)

# Setting labels at the plot.
# First; we want the words at the dots
for i, txt in enumerate(label):
    ax.annotate(txt, (x[i], y[i]))
# and then the text title at the axes
ax.set_xlabel(textTitle1)
ax.set_ylabel(textTitle2)

# a red line at the diagonal to indicate which text uses a word the most
line = mlines.Line2D([0, 1], [0, 1], color='red')
transform = ax.transAxes
line.set_transform(transform)
ax.add_line(line)

plt.show()
