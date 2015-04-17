from text_stream import JsonStream
import gensim
from gensim.models import word2vec, Phrases
import glob
from nltk.corpus import shakespeare
import argparse

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', type=str,
                        help='Directory in which to look for json files containing corpora sentences')
    parser.add_argument('-f', '--file', type=str,
                        help='File containing word2vec model to load')
    parser.add_argument('-s', '--save', type=str, default=None,
                        help='Path to save the model at')

    args = parser.parse_args()

    modeler = Word2VecModeler()
    if args.file is not None:
        modeler.load(args.file)
    elif args.directory is not None:
        corpora = JsonStream(glob.glob(args.directory + '/*.json'))
        modeler.make_model(corpora)
        if args.save is not None:
            modeler.save(args.save)

    print len(modeler.model.vocab)
    print modeler.model.accuracy('./queries/questions-words.txt', restrict_vocab=10000)

if __name__ == '__main__':
    main()
    # corpora = JsonStream(glob.glob('../ug-afs/cs224d-project/elided/amazon_2*.json'))
    # #corpora = word2vec.BrownCorpus('/Users/alex/nltk_data/corpora/brown/')
    # modeler = Word2VecModeler()
    # modeler.make_model(corpora)
    # modeler.save('./models/amazon_2')
    # #modeler.load('./models/brown')
    # print len(modeler.model.vocab)
    # print modeler.model.accuracy('./queries/questions-words.txt', restrict_vocab=10000)
    # #print modeler.model.most_similar(positive=['money', 'cash'], topn=25)