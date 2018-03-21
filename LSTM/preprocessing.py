import numpy as np
import os
from embeddings import Embedding

def generateDatasetFromTokens(tokens, seq_length, embedding):
    vectors = embedding.tokensToVectors(tokens)
    n_tokens = len(tokens)

    dataX = []
    dataY = []
    for i in range(0, n_tokens - seq_length, 1):
        #dataX.append(vectors[i:i + seq_length])
        dataX.append([int(n) for n in tokens[i:i + seq_length]])
        dataY.append(vectors[i + seq_length])

    X = np.reshape(dataX, (len(dataX), seq_length))
    y = np.reshape(dataY, (len(dataY), 300))
    return X, y

def generateDatasetFromString(string, seq_length, embedding):
    tokens = [token for token in string.split(" ") if token != ""]
    return generateDatasetFromTokens(tokens, seq_length, embedding)

#"data/tokenized/mftd_norwegian"
def generateDatasetFromTokenizedDataset(directory, seq_length, embedding):
    basepath = os.path.normpath(os.path.realpath(__file__))
    while os.path.basename(basepath) != "Minerva":
        basepath = os.path.dirname(basepath)
    files = [file for file in os.listdir(os.path.join(basepath, directory)) if file.endswith(".txt")]
    #print(files)
    datasets = []
    for filename in files:
        with open(os.path.join(basepath, "{}/{}".format(directory, filename)), "r") as file:
            datasets.append(file.read())

    keras_ds_x = []
    keras_ds_y = []
    maxDsLength = 5
    for i in range(len(datasets)):
        X, y = generateDatasetFromString(datasets[i], seq_length, embedding)
        keras_ds_x.append(X)
        keras_ds_y.append(y)

        if(len(keras_ds_x) >= maxDsLength):
            # merge and yield
            Xconcat = np.concatenate(keras_ds_x)
            Yconcat = np.concatenate(keras_ds_y)

            yield Xconcat, Yconcat
            keras_ds_x = []
            keras_ds_y = []
    if(len(keras_ds_x) > 0):
        # merge and yield
        Xconcat = np.concatenate(keras_ds_x)
        Yconcat = np.concatenate(keras_ds_y)
        keras_ds_x = []
        keras_ds_y = []
        yield Xconcat, Yconcat




if __name__ == "__main__":
    embedding = Embedding("Norsk_embeddings")
    for ds in generateDatasetFromTokenizedDataset("data/tokenized/mftd_norwegian", 5, embedding):
        print(ds)
