def generateDatasetFromTokens(tokens, seq_length, embedding):
    vectors = self.embedding.tokensToVectors(tokens)
    n_tokens = len(tokens)

    dataX = []
    dataY = []
    for i in range(0, n_tokens - seq_length, 1):
        dataX.append(vectors[i:i + seq_length])
        dataY.append(vectors[i + seq_length])

    X = np.reshape(dataX, (len(dataX), seq_length, 300))
    y = np.reshape(dataY, (len(dataY), 300))
    return X, y

def generateDatasetFromString(string, seq_length, embedding):
    tokens = [token for token in string.split(" ") if token != ""]
    return generateDatasetFromTokens(tokens, seq_length, embedding)
