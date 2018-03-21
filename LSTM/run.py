import numpy as np
from embeddings import Embedding
from model import LSTMModel
import os

basepath = os.path.normpath(os.path.realpath(__file__))
while os.path.basename(basepath) != "Minerva":
    basepath = os.path.dirname(basepath)

embedding = Embedding("Norsk_embeddings")
embeddingMatrix = os.path.join(basepath, "data/tokenized/mftd_norwegian/embeddingMatrix.npy")
seq_length = 5
model = LSTMModel(seq_length, embeddingMatrix, embedding)

checkpoint_dir = "checkpoints"
checkpoint_name = "lstm_basic_embedding"
#model.setCheckpoint(checkpoint_dir, checkpoint_name)
#model.loadCheckpointWithLowestLoss(checkpoint_dir, checkpoint_name)

files = [file for file in os.listdir(os.path.join(basepath, "data/tokenized/mftd_norwegian")) if file.endswith(".txt")]
#print(files)
#with open(os.path.join(basepath, "data/tokenized/mftd_norwegian/{}".format(files[0])), "r") as file:
#    model.fitTextString(file.read(),10, 10)
model.fitTokenizedDataset("data/tokenized/mftd_norwegian", 10, 10)

#tokens = ["Det","var","en","gang","en"]



#print(y.shape[1])


#model.fit(X, y, 10,2)

#print(tokens)
#print(vectors)
