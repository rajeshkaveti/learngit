
from pset_02 import load_datasets
from pset_02.word_embedding import WordEmbedding
import sys
from pset_02 import hashsalt
import pandas as pd
from functools import partial

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
    #print(embedding.embed_document( 'the'))



    #print(my_learn)
    data['learn'] = data['learn'].fillna(value='ZERO')
    data['project'] = data['project'].fillna(value='ZERO')

    learnvecs = data['learn'].apply(embedding.embed_document)
    projvecs = data['project'].apply(embedding.embed_document)

    vectors_lookup = learnvecs + projvecs

    vecs_list = pd.Series(vectors_lookup)
    vectors_df = pd.DataFrame(vectors_lookup, index=vecs_list.index)
    vectors_df.columns = ['vectors']
    #print('##### vectors_df : ', vectors_df)
    print(" vectors_df shape is :: ", vectors_df.shape)

    idx = data.index[data['hashed_id'] == 'b280302a']
    # print ('######## idx.values ######### ', idx.values)

    my_vec = vectors_df.iloc[[idx.values[0]]]
    my_vec = (my_vec.values[0][0])

    #print ("my_vec : ", my_vec)
    print(" my_vec shape is :: ", my_vec.shape)

    distances = vectors_df['vectors'].apply(partial(embedding.my_distance ,my_vec ))


    sortedDistance = distances.sort_values()
    print('###### sortedDistance : ', sortedDistance)


    farDis = sortedDistance.tail(5).index
    for index in farDis:
        print(data.iloc[index])

    nearDis= sortedDistance.head(5).index
    for index in nearDis:
        print(data.iloc[index])
