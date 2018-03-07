import markovify
import datetime
import os

def main():
    
    # input model parameters
    p = {}
    p["directory"] = "../scrapers/text"
    p["sentenceCount"] = 5
    p["comments"] = "first results from simple markovify"

    # get and join all training data
    filenames = getAllFilenames(p["directory"])
    text = joinTexts(p["directory"], filenames)

    # apply markovify and print sentences
    model = makeMarkovModel(text)
    sentences = []
    for i in range(p["sentenceCount"]):
        sentences.append(model.make_sentence())

    # save results to file
    saveResults("results/"+dateStamp()+".txt", p, sentences)

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

def saveResults(filename, p, results):
    with open(filename, 'w') as file:
        file.write("training data:\t" + "../" + p["directory"] + "\n")
        file.write("sentence count:\t" + str(p["sentenceCount"]) + "\n")
        file.write("comments:\t\t" + p["comments"] + "\n")
        file.write("---\n")
        for i in results:
            file.write(i + "\n")

def dateStamp():
    temp = datetime.datetime.now()
    return "%04d" % temp.year + "%02d" % temp.month + "%02d" % temp.day + "%02d" % temp.hour + "%02d" % temp.minute + "%02d" % temp.second

if __name__ == '__main__':
    main()
