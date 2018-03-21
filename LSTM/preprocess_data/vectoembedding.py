from gensim.models import KeyedVectors

embedding = KeyedVectors.load_word2vec_format('newvec.vec', binary=False)
embedding.save("outofvocabonly")
