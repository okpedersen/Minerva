import markovify
import os

def loadData(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

def getAllFilenames(directory):
    filenames = []
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            filenames.append(file)
    return filenames

def joinTexts(directory, filenames):
    allText = ""
    for filename in filenames:
        allText += " " + loadData(directory+"/" +filename)
    return allText

def makeMarkovModel(text):
    return markovify.Text(text)


directory = "../scrapers/text"
filenames = getAllFilenames(directory)
text = joinTexts(directory, filenames)

model = makeMarkovModel(text)
for i in range(5):
    sentence = model.make_sentence()
    print()
    print(sentence)
