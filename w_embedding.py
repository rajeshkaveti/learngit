import pandas as pd
import numpy as npy
import xlrd
import re

def load_words(filename):
    with open(filename, "r") as fd:
        lines = fd.read().splitlines()
    return lines

def load_data(filename):
    data = pd.read_excel(filename,0)
    return data


def load_vectors(filename):
    vector = npy.load(filename)
    return vector

def tokenize(text):
    # Get all "words", including contractions
    # eg tokenize("Hello, I'm Scott") --> ['Hello', "I'm", "Scott"]
    return re.findall("\w[\w']+", text)

def cos_sim(a, b):
	"""Takes 2 vectors a, b and returns the cosine similarity according 
	to the definition of the dot product
	"""
	dot_product = npy.dot(a, b)
	norm_a = npy.linalg.norm(a)
	norm_b = npy.linalg.norm(b)
	return dot_product / (norm_a * norm_b)

class WordEmbedding(object):
    
    def __init__(self, words, vector):
       self.words=words
       self.vector=vector

    def __call__(self, word):
        """Embed a word

        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """
        try:
            wordIndex=self.words.index(word.lower())
            return self.vector[wordIndex]
        except ValueError:
            return None
        
    
        # Consider how you implement the vocab lookup.  It should be O(1).
        

    @classmethod
    def from_files(cls, word_file, vec_file):
        """Instanciate an embedding from files

        Example::

            embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')

        :rtype: cls
        """
        return cls(load_words(word_file), load_vectors(vec_file))
    
           
    def embed_document(self, text):
        """Convert text to vector, by finding vectors for each word and combining
        :param str document: the document (one or more words) to get a vector
            representation for
        :return: vector representation of document
        :rtype: ndarray (1D)
        """


        words = tokenize(text)
        ret_array = embedding(words[0])
        if ret_array is None:
            ret_array = npy.zeros((len(words), 300))
        for word in words:
            dim = embedding(word)
            if dim is None:
                pass
            else:
                ret_array = npy.add(ret_array, dim)
            # Use tokenize(), maybe map(), functools.reduce, itertools.aggregate...
            # Assume any words not in the vocabulary are treated as 0's
            # Return a zero vector even if no words in the document are part
            # of the vocabulary
        return ret_array

words=load_words("words.txt")
vector = load_vectors("vectors.npy.gz")

wordEmbedding = WordEmbedding.from_files("words.txt","vectors.npy.gz")
print(wordEmbedding("a'nd"))
#print(wordEmbedding("the1"))

embedding = WordEmbedding(words,vector)
data = load_data("hashed.xlsx")
data.set_index('hashed_id')
data['learn'] = data['learn'].fillna(value='ZERO')
data['project'] = data['project'].fillna(value='ZERO')


#vec=wordEmbedding.embed_document(data['project'][4])
#print(vec.shape)

#data['learn'].dropna(inplace=True)

learnvecs = data['learn'].apply(wordEmbedding.embed_document) 
projvecs = data['project'].apply(wordEmbedding.embed_document) 

print ("len of data.learn ***********" , len(data['learn']))
print ("len of data.project ***********" , len(data['project']))

print ("learn shape : ", learnvecs.shape)
print ("project shape : ", projvecs.shape)

#print (learnvecs)

#print (data['learn'])
#print ('************')
#print (data['project'])


vecs = learnvecs+ projvecs
print(vecs.shape)

df = pd.DataFrame([v for v in vecs.values], index=vecs.index)
print(df)

first_elem = vector[0]
second_elem = vector[1]

#print ("First element : ", first_elem)
#print ("Second element : ", second_elem)

print(cos_sim(first_elem, second_elem))
