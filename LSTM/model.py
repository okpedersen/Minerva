import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint

class LSTMModel:
    def __init__(self, shape1, shape2, outShape):
        self.model = Sequential()
        self.model.add(LSTM(256, input_shape=(shape1, shape2), return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(256))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(outShape, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')

    def fit(self):
        model.fit(X, y, epochs=50, batch_size=64, callbacks=callbacks_list)


model1 = LISTModel(2,3,3)

model2 = LISTModel(5,1,2)

model1.fit()
