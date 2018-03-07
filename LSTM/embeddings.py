from gensim.models import KeyedVectors
import numpy as np

#model = KeyedVectors.load('../cc.no.300.vec')
class Embedding:

    def __init__(self, embeddingFile):
        self.model = KeyedVectors.load(embeddingFile)

    def wordToVector(self, word):
        try:
            return self.model.word_vec(word)
        except KeyError:
            pass # Word not in vocabulary

        try:
            return self.model.word_vec(word.lower()) #Try with lowercase
        except KeyError:
            pass #Out of vocabulary

        """
        TODO: Handle out of vocabulary words
        """



    def vectorToWord(self, vector):
        word = self.model.similar_by_vector[vector][0][0]
        return word

    def getClosestWordVector(self, vector):
        word = self.vectorToWord(vector)
        return word, self.model.word_vec(word)

    def tokensToVectors(self, tokens):
        vectors = np.empty([len(tokens), 300])
        for i, token in enumerate(tokens):
            vectors[i,:] = self.wordToVector(token)

        return vectors
