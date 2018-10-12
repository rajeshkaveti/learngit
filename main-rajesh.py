
from pset_02 import load_datasets
from pset_02.word_embedding import WordEmbedding
import sys
from pset_02 import hashsalt
import pandas as pd

if __name__ == '__main__':
    SALT = sys.argv[1]
    CSCI_SALT = bytes.fromhex(SALT)
    hash_id = hashsalt.hash_str('rajeshkaveti', CSCI_SALT)
    print(hash_id)
    my_hash = hash_id[:8].strip()

    words = load_datasets.load_words("data/words.txt")
    vector = load_datasets.load_vectors("data/vectors.npy.gz")
    data = load_datasets.load_data("data/hashed.xlsx")
    data.set_index('hashed_id')

    #wordEmbedding = word_embedding.WordEmbedding.from_files("data/words.txt",  "data/vectors.npy.gz")

    embedding = WordEmbedding(words, vector)
    print(embedding.embed_document('the'))


    my_row = data[data['hashed_id'] == my_hash]
    my_project = my_row['project']
    my_learn = my_row['learn']
    print(my_project)
    #print(my_learn)
    data['learn'] = data['learn'].fillna(value='ZERO')
    data['project'] = data['project'].fillna(value='ZERO')
    #print(data['learn'])
    learnvecs = data['learn'].apply(embedding.embed_document)
    #print(learnvecs)
    # learnvecs = embedding.embed_document(data['learn'][3])
    learnvecs = learnvecs.ravel()
    #print(learnvecs.shape)
    projvecs = data['project'].apply(embedding.embed_document)
    projvecs = projvecs.ravel()

