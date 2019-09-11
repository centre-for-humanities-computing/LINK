#!/home/knielbo/virtenvs/LINK/bin/python
import numpy as np
import os
import random
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import mutual_info_classif

from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt


def get_idxs(lst, val):
    return [i for i, x in enumerate(lst) if x == val]


def vect_transform(texts, analyzer_lvl = "word", min_df = 2, mx_feat = 10, ngram_rng = (1, 1), stop_words = "english"):
    vectorizer = CountVectorizer(
            analyzer=analyzer_lvl,
            min_df=min_df,
            max_features=mx_feat,
            ngram_range=ngram_rng,
            stop_words=stop_words
            )

    dtm = vectorizer.fit_transform(texts)
    lexicon = vectorizer.get_feature_names()
    
    return dtm, lexicon




datpath = os.path.join("DATA", "CLASS_DATA.csv")
corpus = pd.read_csv(datpath, index_col=0)
texts = corpus["text"].tolist()
y = corpus["class"].tolist()
fnames = corpus.index.tolist()
X, lexicon = vect_transform(texts)




"""
clf = LogisticRegression(random_state=0, solver='lbfgs').fit(X, y)


print("accuracy = {}".format(clf.score(X, y)))

y_prop = clf.predict_proba(X)





## baseline
random_y = random.sample(y, len(y))
clf = LogisticRegression(random_state=0, solver='lbfgs').fit(X, random_y)

print(clf.score(X, random_y))


# baseline figure


rand_acc = list()
acc = list() 
for i in range(40):
    clf = LogisticRegression(random_state=i, solver='lbfgs').fit(X, y)
    acc.append(clf.score(X, y))
print(acc)
"""




# prediction figure
clf = LogisticRegression(random_state=0, solver='lbfgs').fit(X, y)
y_prop = clf.predict_proba(X)

col = 0
labels = sorted(list(set(y)))[::-1]
start = 0
color = ["r", "g"]
marker = ["v", "o"]
for i, label in enumerate(labels):
    idxs = get_idxs(y, label)
    y1 = [y_prop[idx, col] for idx in idxs]
    

    x = list(range(start, start + len(y1)))
    plt.plot(x,y1, color=color[i], marker=marker[i], linestyle="", label=label)
    start = max(x) + 1
plt.ylabel("P({})".format(labels[col+1]))
plt.legend()
plt.tight_layout()
plt.savefig("FIGS/classification.png", dpi=300)
plt.close()



