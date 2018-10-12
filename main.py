from w_embedding import *


if __name__ == '__main__':

    embedding = WordEmbedding.from_files("words.txt" , "vectors.npy.gz")

    a = embedding.embed_document("test this")

    print(a)