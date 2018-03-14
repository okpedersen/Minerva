from gensim.models import KeyedVectors
import fastText as ft
import numpy as np
import os
import sys

print("loading vocabulary")
embeddings = KeyedVectors.load("Norsk_embeddings")
print("loading out of vocabulary")
outofvocab = ft.load_model("norsk.bin")
print("loading data")
basepath = os.path.normpath(os.path.realpath(__file__))
while os.path.basename(basepath) != "Minerva":
    basepath = os.path.dirname(basepath)

directory = os.path.normpath(os.path.join(basepath, "data/clean/mftd_norwegian"))


newWords = {}
seen = set()
print("Loaded data")
for filename in os.listdir(directory):
    with open(directory+"/"+filename, 'r') as file:
        data = file.read()
    tokens = [token for token in data.split(" ") if token != ""]
    for token in tokens:
        if token in seen:
            continue
        seen.add(token)
        try:
            embeddings.word_vec(token)
            continue
        except KeyError:
            pass # Word not in vocabulary
        try:
            embeddings.word_vec(token.lower()) #Try with lowercase
            continue
        except KeyError:
            pass #Out of vocabulary

        newWords[token] = outofvocab.get_word_vector(token)


if len(newWords) == 0:
    print("No out of vocabulary words detected")
    sys.exit()

else:
    print("{} out of vocabulary words found:\n\n".format(len(newWords)))

newLines = ""
newWordString = ""
for newword in newWords:
    newWordString += newword + '\n'
    line = str(newword) + " "+np.array2string(newWords[newword], formatter={'float_kind':lambda x: "%.4f" % x})[1:-1].replace('\n','') +"\n"
    newLines += line
print("writing to file")
with open("outofvocablist.txt", 'w') as file:
    file.write(newWordString)
with open("300novec.vec", 'a') as file:
    file.write(newLines)
