#!/home/knielbo/virtenvs/LINK/bin/python

import io
import os
from pandas import DataFrame



def read_dir(path):
    textls, filenamels = list(), list()
    for (root, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            with open(filepath, "r") as f:
                text = f.read()
            textls.append(text)
            filenamels.append(filename.split(".")[0])
    return textls, filenamels

def make_df(path, classification):
    texts, fnames = read_dir(path)
    rows = []
    idx = []
    for i, text in enumerate(texts):
        rows.append({'text': text, 'class': classification})
        idx.append(fnames[i])
        i += 1
    df = DataFrame(rows, index = idx)
    return df

def main():
    NT = 'new_testament'
    OT = 'old_testament'
    SRCS = [("DATA/KJV/OT", OT),("DATA/KJV/NT", NT)]
    DATA = DataFrame({'text': [], 'class': []})
    for path, classification in SRCS:
        DATA = DATA.append(make_df(path, classification))
    DATA.to_csv("DATA/CLASS_DATA.csv")

if __name__ == main:
    main()
