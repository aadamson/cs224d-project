from text_stream import JsonStream
import gensim
from gensim.models import word2vec, Phrases
import glob

class Modeler(object):
    def __init__(self):
        self.model = None

    def make_model(self, *args):
        pass

class Word2VecModeler(Modeler):
    def __init__(self):
        super(Word2VecModeler, self).__init__()

    def load(self, fname):
        self.model = word2vec.Word2Vec.load(fname)

    def make_model(self, corpora):
        #bigram_transformed = gensim.models.Phrases(corpora)
        self.model = word2vec.Word2Vec(corpora, size=10, window=5, min_count=5, workers=4)

    def save(self, fname):
        if self.model is not None:
            self.model.save(fname)
