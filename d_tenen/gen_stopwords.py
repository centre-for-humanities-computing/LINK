import nltk
from nltk.corpus import stopwords

for word in sorted(list(set(stopwords.words('english')))):
    print(word)
