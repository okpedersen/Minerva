import numpy as np
from embeddings import Embedding
from model import LSTMModel

embedding = Embedding("Norsk_embeddings")
seq_length = 2
model = LSTMModel(seq_length, embedding)

checkpoint_dir = "checkpoints"
checkpoint_name = "lstm_basic_embedding"
model.setCheckpoint(checkpoint_dir, checkpoint_name)
model.loadCheckpointWithLowestLoss(checkpoint_dir, checkpoint_name)


tokens = ["Det","var","en","gang","en"]



print(y.shape[1])


model.fit(X, y, 10,2)

#print(tokens)
#print(vectors)
