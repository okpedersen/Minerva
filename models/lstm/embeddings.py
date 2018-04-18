from gensim.models import KeyedVectors
import numpy as np
import random

#model = KeyedVectors.load('../cc.no.300.vec')
class Embedding:

    def __init__(self, embeddingFile):
        self.filename = embeddingFile
        self.loadedEmbedding = False

    def loadEmbeddingFromFile(self):
        self.model = KeyedVectors.load(self.filename)
        self.loadedEmbedding = True

    def unloadEmbedding(self):
        del self.model
        import gc
        gc.collect()
        self.loadedEmbedding = False

    def wordToVector(self, word):
        if not self.loadedEmbedding:
            self.loadEmbeddingFromFile()
        try:
            return self.model.word_vec(word)
        except KeyError:
            pass # Word not in vocabulary

        return self.model.word_vec(word.lower()) #Try with lowercase
        #except KeyError:
        #    pass #Out of vocabulary




    def vectorToWord(self, vector):
        if not self.loadedEmbedding:
            self.loadEmbeddingFromFile()
        potRes = self.model.similar_by_vector(vector)[0:5]
        return potRes[0][0]
        probSum = 0
        for pres in potRes:
            probSum += pres[1]

        for i in range(len(potRes)):
            potRes[i] = list(potRes[i])
            potRes[i][1] /= probSum
        prob = random.random()
        cumProb = 0
        idx = -1
        while(cumProb < prob):
            idx += 1
            cumProb += potRes[idx][1]

        return potRes[idx][0]

    def getClosestWordVector(self, vector):
        if not self.loadedEmbedding:
            self.loadEmbeddingFromFile()
        word = self.vectorToWord(vector)
        return word, self.model.word_vec(word)

    def tokensToVectors(self, tokens):
        vectors = np.empty([len(tokens), 300])
        for i, token in enumerate(tokens):
            vectors[i,:] = self.wordToVector(token)

        return vectors
