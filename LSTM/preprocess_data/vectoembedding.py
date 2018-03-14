from gensim.models import KeyedVectors

embedding = KeyedVectors.load_word2vec_format('300novec.vec', binary=False)
embedding.save("Norske_eventyr")
