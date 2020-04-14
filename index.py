from document import *
import math
from operator import itemgetter
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()



class Index:
    """An inverted index."""

    def __init__(self):
        """Creates the index.

        Args:
        - self: this index, the one to create. mandatory object reference.

        Returns:
        None.
        """
        self.index = dict() # inverted index main dictionary with word as key and a tuple of document id and count of word in that document
        self.CountWords = dict() #keeps count of number of words in each document
        self.N = 0 #keeps count of the number of documents added s

    def add_doc(self, doc: Document) -> None:
        """Adds doc to the index.

        Args:
        - self: this index, the one to add to. mandatory object reference.
        - doc: the document to add.

        Returns:
        None.
        """
        self.N+=1
        i = 0
        for word, loc in doc.words():
          i += 1 #number of processed words in doc
          word = index_preprocess(word)
          if word:
            self.index[word] = self.index.get(word, []) + [(doc.doc_id, len(loc))]
        if i:
          self.CountWords[doc.doc_id] = self.CountWords.get(doc.doc_id, 0) + i
        else:
          self.CountWords[doc.doc_id] = 1
          

    def query(self, query_string: str) -> [(str, float)]:
        """Returns a ranked list of document IDs from the index and their TF-IDF score
        for query_string. The ranking is from most similar (index 0) to least similar.

        Args:
        - self: this index, the one to search in. mandatory object reference.
        - query_string: contains space separated query words

        Returns:
        A list of pairs where each pair contains a document ID and the TF-IDF of
        the corresponding document with query_string. The list is sorted in
        order to decreasding similarity.
        """
        #tf-idf(t, d) = tf(t, d) * log(N/(df + 1))
        #tf(t,d) = count of t in d / number of words in d
        #df(t) = occurrence of t in documents
        df = 0
        TF_IDF = dict() #the final result dictionary
        query_string = query_tokenize(query_string)
        for word in query_string:
          df = len(self.index.get(word, []))
          if not df:
            df = 1
          for docId, count in self.index.get(word,[]):
            tf = count/self.CountWords[docId]
            tf_idf = tf * math.log(self.N/df, 10)
            TF_IDF[docId] = TF_IDF.get(docId, 0) + tf_idf
        return sorted(TF_IDF.items(), key=itemgetter(1), reverse = True)


        

# ------------------------- Helpers -------------------------


def index_preprocess(word: str) -> str:
    """Returns a processed version of word appropriate for adding to the index.

    Implement as you wish. The default returns word as is.

    Args:
    - word: the potential word to be processed for indexing.

    Returns:
    An appropriately processed version of word.
    """
    #stems each word before indexing
    if len(word) > 1:
      word = stemmer.stem(word)
    return word if len(word) > 1 else ""

def query_tokenize(query_string: str):
    """Returns a list of query words tokenized from query_string, appropriate
    for querying the index.

    Implement as you wish. The default splits query_string at whitespace.

    Args:
    - query_string: the string to tokenize.

    Returns:
    A list of query tokens appropriate for querying the index.
    """
    query_string = query_string.lower()
    query_string = query_string.replace("'", "") #removing apostrophe
    special_char = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n" #replacing special characters and punctuations with empty space
    for i in special_char:
      query_string = query_string.replace(i , " ")

    query_string = query_string.split()
    query_string = [index_preprocess(word) for word in query_string] #each word in query_string is stemmed
    return query_string
