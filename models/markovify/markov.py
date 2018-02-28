import markovify
import datetime
import os

def main():

    # get the root directory of the Minerva project
    # e.g. /something/something/Minerva
    basepath = os.path.normpath(os.path.realpath(__file__))
    while os.path.basename(basepath) != "Minerva":
        basepath = os.path.dirname(basepath)

    # input model parameters
    p = {}
    p["method"] = "markovify"
    p["stateSize"] = 4
    p["directory"] = os.path.normpath(os.path.join(basepath, "data/raw/mftd_english"))
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

    # save results to file
    saveResults(os.path.join(basepath, "results", dateStamp()+".txt"), p, sentences)

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
        allText += " " + loadData(os.path.join(directory,filename))
    return allText

def makeMarkovModel(text, stateSize):

    return markovify.Text(text, state_size = stateSize)

def saveResults(filename, p, results):
    print("Writing to: " + filename)
    with open(filename, 'w') as file:
        file.write("method:\t\t" + p["method"] + "\n")
        file.write("training data:\t" + p["directory"] + "\n")
        file.write("sentence count:\t" + str(p["sentenceCount"]) + "\n")
        file.write("comments:\t" + p["comments"] + "\n")
        file.write("---\n")
        for i in results:
            if i is not None:
                file.write(i + "\n")

def dateStamp():
    temp = datetime.datetime.now()
    return "{t.year:04d}{t.month:02d}{t.day:02d}{t.hour:02d}{t.minute:02d}{t.second:02d}".format(t=temp)

if __name__ == '__main__':
    main()
