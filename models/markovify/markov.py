import markovify
import datetime
import os

def main():
    
    # input model parameters
    p = {}
    p["method"] = "markovify"
    p["stateSize"] = 1
    p["directory"] = "../../data/raw/facebook"
    p["sentenceCount"] = 10
    p["comments"] = "n.a."

    # get and join all training data
    filenames = getAllFilenames(p["directory"])
    text = joinTexts(p["directory"], filenames)

    # apply markovify and print sentences
    model = makeMarkovModel(text, p["stateSize"])
    sentences = []
    for i in range(p["sentenceCount"]):
        sentences.append(model.make_sentence())

    # # save results to file
    # saveResults(dateStamp()+".txt", p, sentences)

    for i in sentences:
        print(str(i)+"\n")

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

def makeMarkovModel(text, stateSize):

    return markovify.Text(text, state_size = stateSize)

def saveResults(filename, p, results):
    with open("../../results/"+filename, 'w') as file:
        file.write("method:\t\t" + p["method"] + "\n")
        file.write("training data:\t" + "../" + p["directory"] + "\n")
        file.write("sentence count:\t" + str(p["sentenceCount"]) + "\n")
        file.write("comments:\t" + p["comments"] + "\n")
        file.write("---\n")
        for i in results:
            file.write(i + "\n")

def dateStamp():
    temp = datetime.datetime.now()
    return "%04d" % temp.year + "%02d" % temp.month + "%02d" % temp.day + "%02d" % temp.hour + "%02d" % temp.minute + "%02d" % temp.second

if __name__ == '__main__':
    main()
