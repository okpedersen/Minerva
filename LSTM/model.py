import numpy as np
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Embedding
from keras.callbacks import ModelCheckpoint
from preprocessing import generateDatasetFromTokens
from preprocessing import generateDatasetFromString


class LSTMModel:
    def __init__(self, seqLen, embeddingMatrixFile, embedding = None):
        self.embedding = embedding
        self.seq_length = seqLen

        embeddingMatrix = np.load(embeddingMatrixFile)
        self.model = Sequential()
        self.model.add(Embedding(embeddingMatrix.shape[0], embeddingMatrix.shape[1], weights=[embeddingMatrix],
        input_length=seqLen, trainable=False))
        self.model.add(LSTM(256, input_shape=(seqLen, 300), return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(256))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(300, activation='softmax'))
        self.model.compile(loss='cosine_proximity', optimizer='adam')
        self.currentEpoch = 0

        self.callbacks_list = []

    def loadCheckpoint(self, filepath):
        print("Loaded checkpoint {}".format(filepath))
        self.model.load_weights(filepath)

    def loadCheckpointWithLowestLoss(self, directory, name):
        checkpointFiles = [file[len(name) +1:-5] for file in os.listdir(directory) if file.startswith(name) and file.endswith(".hdf5")]
        if len (checkpointFiles) < 1:
            return

        lowestLoss = float('inf')
        checkpoint = ""
        for file in checkpointFiles:
            if(float(file) < lowestLoss):
                lowestLoss = float(file)
                checkpoint = file

        self.loadCheckpoint("{}/{}-{}.hdf5".format(directory,name,checkpoint))

    def setCheckpoint(self, directory, name):
        filepath = directory+"/"+name+"-{loss:.8f}.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        self.callbacks_list.append(checkpoint)

    def fit(self, X, y, epochs, batch_size):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size)#, callbacks=self.callbacks_list

    def fitTextTokens(self, tokens, epochs, batch_size):
        X, y = generateDatasetFromTokens(tokens, self.seq_length, self.embedding)
        self.fit(X, y, epochs, batch_size)

    def fitTextString(self, string, epochs, batch_size):
        X, y = generateDatasetFromString(string, self.seq_length, self.embedding)
        print(X.shape)
        self.fit(X, y, epochs, batch_size)
    """
    def fitTextString(self, string, epochs, batch_size):
        X, y = generateDatasetFromString(string, self.seq_length, self.embedding)
        self.fit(X, y, epochs, batch_size)
        """

    def predictNextWord(self, vectors):
        prediction = model.predict(x, verbose=0)
        word, vector = self.embedding.getClosestWordVector(prediction)

    def generateText(self, seed, numWords = 100):
        pass
