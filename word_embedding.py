import pandas as pd
import numpy as npy
#from hashsalt import *
import xlrd
import re
import os
import sys
import hashlib


class WordEmbedding(object):

    def __init__(self, words, vector):
        self.words = words
        self.vector = vector

    def __call__(self, word):
        """Embed a word

        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """
        try:
            # print("Inside call function ***" , word)
            wordIndex = self.words.index(word.lower())
            # print(wordIndex)
            # print(self.vector[wordIndex])
            return self.vector[wordIndex]
        except ValueError:
            #print('errir')
            return None
        # Consider how you implement the vocab lookup.  It should be O(1).

    @classmethod
    def from_files(cls, word_file, vec_file):
        """Instanciate an embedding from files

        Example::

            embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')
|
        :rtype: cls
        """
        return cls(load_words(word_file), load_vectors(vec_file))

    def embed_document(self,text):
        words = self.tokenize(text)

        sent_vec = npy.zeros((1, 300))

        for w in words:
            try:
                vc = self(w)
                #                 print(vc[0])
                sent_vec = npy.add(sent_vec, vc)
            #                 print(sent_vec[0][0])
            except:
                pass
        # print(sent_vec)
        return sent_vec

    def tokenize(self,text):
        # Get all "words", including contractions
        # eg tokenize("Hello, I'm Scott") --> ['Hello', "I'm", "Scott"]
        return re.findall("\w[\w']+", text)


    def cosine_similarity(self, a, b):
        dot_product = npy.dot(a[0], b.T)
        #print(dot_product)
        norm_a = npy.linalg.norm(a)
        norm_b = npy.linalg.norm(b)
        #print(norm_a)
        #print(norm_b)
        #print((norm_a * norm_b))
        return dot_product / (norm_a * norm_b)

    def my_distance(self , vec , my_vec):

        return 1 - self.cosine_similarity(vec, my_vec)

    def cos_sim(a, b):
        """Takes 2 vectors a, b and returns the cosine similarity according
        to the definition of the dot product
        """
        dot_product = npy.dot(a, b)
        norm_a = npy.linalg.norm(a)
        norm_b = npy.linalg.norm(b)
        return dot_product / (norm_a * norm_b)
