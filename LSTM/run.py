import sys
if len(sys.argv) <= 1:
    print("Specify a config file")
    sys.exit()
import json

with open(sys.argv[1],'r') as file:
    config = json.loads(file.read())


import numpy as np
from embeddings import Embedding
from model import LSTMModel
import os


basepath = os.path.normpath(os.path.realpath(__file__))
while os.path.basename(basepath) != "Minerva":
    basepath = os.path.dirname(basepath)

embeddingPath = os.path.join(basepath, "LSTM/preprocess_data/{}".format("outofvocabonly"))

embedding = Embedding(embeddingPath)
embeddingMatrix = os.path.join(basepath, "data/tokenized/mftd_norwegian/embeddingMatrix.npy")
seq_length = config["seq_length"]
model = LSTMModel(seq_length, embeddingMatrix, config["layers"], config["dropout_layers"], config["action"], embedding)

if(config["use-checkpoint"]):
    checkpoint_dir = "checkpoints/"+config["checkpoint_dir"]
    checkpoint_name = "lstm_basic_embedding"
    if config["action"] == "train":
        model.setCheckpoint(checkpoint_dir, checkpoint_name, config["checkpoint_interval"])
    model.loadCheckpointWithLowestLoss(checkpoint_dir, checkpoint_name)


if config["action"] == "train":
    model.fitTokenizedDataset("data/clean/mftd_norwegian", config["epochs"], config["batch_size"])
elif config["action"] == "test":
    seed = config["seed"]
    initText = " ".join(seed.split(" ")[:config["seq_length"]])
    print(initText, end="")
    text = model.generateText(seed, 300)
