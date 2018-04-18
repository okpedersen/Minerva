import numpy as np
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Embedding
from keras.callbacks import ModelCheckpoint
from preprocessing import generateDatasetFromTokens
from preprocessing import generateDatasetFromString
from preprocessing import generateDatasetFromTokenizedDataset
from keras.layers.normalization import BatchNormalization

class LSTMModel:
    def __init__(self, seqLen, embeddingMatrixFile, layers, dropout_layers, action, embedding = None):
        self.embedding = embedding
        self.seq_length = seqLen
        self.special_words = ['.', ',', ':', ';', '[', ']', '(', ')', '"']

        embeddingMatrix = np.load(embeddingMatrixFile)
        if action == "train":
            statefulConfig = False
        else:
            statefulConfig = True

        self.model = Sequential()
        isMoreThanOneLayer = len(layers) > 1
        if statefulConfig:
            self.model.add(LSTM(layers[0], batch_input_shape=(1, seqLen, 300), return_sequences=isMoreThanOneLayer, stateful=True))
            self.model.add(Dropout(dropout_layers[0]))
        else:
            self.model.add(LSTM(layers[0], input_shape=(seqLen, 300), return_sequences=isMoreThanOneLayer, stateful=False))
            self.model.add(Dropout(dropout_layers[0]))

        for layerN in range(1, len(layers)):
            notLastLayer = (len(layers) - 1) > layerN
            self.model.add(LSTM(layers[layerN], stateful=statefulConfig, return_sequences=notLastLayer))
            self.model.add(Dropout(dropout_layers[layerN]))





        #self.model.add(BatchNormalization())
        #self.model.add(Dropout(0.2))
        #self.model.add(LSTM(256, stateful=True))
        #self.model.add(Dropout(0.2))
        self.model.add(Dense(300))
        #self.model.add(BatchNormalization())
        self.model.compile(loss='cosine_proximity', optimizer='adam')
        #self.model.compile(loss='mse', optimizer='adam')
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

    def setCheckpoint(self, directory, name, checkpoint_interval):
        filepath = directory+"/"+name+"-{loss:.8f}.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min', period=checkpoint_interval)
        self.callbacks_list.append(checkpoint)

    def fit(self, X, y, epochs, batch_size):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, callbacks=self.callbacks_list, shuffle = False)#

    def fitTextTokens(self, tokens, epochs, batch_size):
        X, y = generateDatasetFromTokens(tokens, self.seq_length, self.embedding)
        self.fit(X, y, epochs, batch_size)

    def fitTextString(self, string, epochs, batch_size):
        X, y = generateDatasetFromString(string, self.seq_length, self.embedding)
        print(X.shape)
        self.fit(X, y, epochs, batch_size)

    def fitTokenizedDataset(self, directory, epochs, batch_size):
        for X, y, n_datasets in generateDatasetFromTokenizedDataset(directory, self.seq_length, self.embedding):
            self.fit(X, y, epochs, batch_size)
        """
        for epoch in range(epochs):

            print("Starting epoch {}/{}".format(epoch+1, epochs))
            count = 1
            for X, y, n_datasets in generateDatasetFromTokenizedDataset(directory, self.seq_length, self.embedding):
                print("Fitting part {} of epoch".format(count))
                if(count < n_datasets):
                    self.model.fit(X, y, epochs=1, batch_size=batch_size, shuffle = False)
                else:
                    self.fit(X, y, 1, batch_size)
                count += 1
        """

    """
    def fitTextString(self, string, epochs, batch_size):
        X, y = generateDatasetFromString(string, self.seq_length, self.embedding)
        self.fit(X, y, epochs, batch_size)
        """

    def predictNextWord(self, prediction):
        #prediction = model.predict(x, verbose=0)
        word, vector = self.embedding.getClosestWordVector(prediction)
        return word, vector

    def generateText(self, seed, numWords = 2000):
        X, _ = generateDatasetFromString(seed, self.seq_length, self.embedding)
        out = []
        #print(X.shape)
        for i in range(numWords):
            pred = self.model.predict(X)[0]
            word, vector = self.predictNextWord(pred)
            out.append(word)
            if word in self.special_words:
                print(word,end="", flush=True)
            else:
                print(" {}".format(word), end="", flush=True)

            X = np.concatenate((X[:,1:,:], np.reshape(vector,(1,1,300))), axis=1)
        return " ".join(out)
