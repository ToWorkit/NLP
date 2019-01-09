import math

from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import *
from collections import Counter

text1 = "Python is a 2000 made-for-TV horror movie directed by Richard \
Clabaugh. The film features several cult favorite actors, including William \
Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy, \
Keith Coogan, Robert Englund (best known for his role as Freddy Krueger in the \
A Nightmare on Elm Street series of films), Dana Barron, David Bowe, and Sean \
Whalen. The film concerns a genetically engineered snake, a python, that \
escapes and unleashes itself on a small town. It includes the classic final\
girl scenario evident in films like Friday the 13th. It was filmed in Los Angeles, \
 California and Malibu, California. Python was followed by two sequels: Python \
 II (2002) and Boa vs. Python (2004), both also made-for-TV films."

text2 = "Python, from the Greek word (πύθων/πύθωνας), is a genus of \
nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are \
recognised.[2] A member of this genus, P. reticulatus, is among the longest \
snakes known."

text3 = "The Colt Python is a .357 Magnum caliber revolver formerly \
manufactured by Colt's Manufacturing Company of Hartford, Connecticut. \
It is sometimes referred to as a \"Combat Magnum\".[1] It was first introduced \
in 1955, the same year as Smith &amp; Wesson's M29 .44 Magnum. The now discontinued \
Colt Python targeted the premium revolver market segment. Some firearm \
collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy \
Thompson, Renee Smeets and Martin Dougherty have described the Python as the \
finest production revolver ever made."

def get_tokens(text):
    texts = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(texts)

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def gen_count(text):
    t1_words = get_tokens(text)
    stemmer = PorterStemmer()
    stemmed = stem_tokens(tokens = t1_words, stemmer = stemmer)
    filter = [word for word in stemmed if word not in stopwords.words('english')]
    count = Counter(stemmed)
    return count
print(stopwords.words('english'))

def tf(word, count):
    return count[word] / max(count.values())

def df(word, count_list):
    return sum(1 for count in count_list if word in count)

def idf(word, count_list):
    return math.log(len(count_list) / (df(word, count_list) + 1))

def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)

count_lst = [gen_count(text1), gen_count(text2), gen_count(text3)]

for i, count in enumerate(count_lst):
    print("每个文档中分值高的前几个word: {}".format(i + 1))
    scores = { word: tfidf(word, count, count_lst) for word in count }
    sorted_words = sorted(scores.items(), key = lambda x: x[1], reverse = True)
    for word, score in sorted_words[:3]:
        print("\t Word: {}, TF-IDF: {}".format(word, round(score, 5)))