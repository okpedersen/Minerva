from preprocessing import generateDatasetFromString
from gensim.models import KeyedVectors
from embeddings import Embedding
import os
import numpy as np
import gc

seqLen = 10
embedding = Embedding('preprocess_data/outofvocabonly')
basepath = os.path.normpath(os.path.realpath(__file__))
while os.path.basename(basepath) != "Minerva":
    basepath = os.path.dirname(basepath)

directory = os.path.normpath(os.path.join(basepath, "data/clean/mftd_norwegian"))
directoryOut = os.path.normpath(os.path.join(basepath, "data/tokenized/mftd_norwegian"))

seenWords = set()
wordList = []
xs = []
ys = []
for filename in os.listdir(directory):
    with open(directory+"/"+filename, 'r') as file:
        data = file.read().split()
        for word in data:
            if word not in seenWords:
                seenWords.add(word)
                wordList.append(word)

word2index = {k:i for i,k in enumerate(wordList)}
embeddingMatrix = np.zeros((len(wordList),300))
for i, word in enumerate(wordList):
    embeddingMatrix[i] = embedding.wordToVector(word)

#write embedding to file and clear memory!
del embedding
np.save(os.path.normpath(os.path.join(basepath, "data/tokenized/mftd_norwegian/embeddingMatrix.npy")), embeddingMatrix)
del embeddingMatrix
gc.collect()

for filename in os.listdir(directory):
    with open(directory+"/"+filename, 'r') as file:
        data = file.read().split()
        tokenizedText = ""
        for word in data:
            tokenizedText += str(word2index[word])+" "
        with open(directoryOut+"/"+filename, 'w') as file2:
            file2.write(tokenizedText)

outWordListStr = ""
for word in wordList:
    outWordListStr += word+"\n"
with open(directoryOut+"/"+"word2index.txt", 'w') as file2:
    file2.write(outWordListStr)




#input()
    #xs.append(X)
    #ys.append(y)
#outX = np.array(xs)
#outY = np.array(ys)
#np.save(os.path.normpath(os.path.join(basepath, "data/clean/no_X.npy")), outX)
#np.save(os.path.normpath(os.path.join(basepath, "data/clean/no_Y.npy")), outY)
