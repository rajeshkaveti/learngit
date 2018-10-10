# -*- coding: utf-8 -*-

import luigi
from luigi import *
#from luigi import Task
import pandas as pd
from pset.tasks.embeddings.load_embeding import EmbedStudentData
from pset.tasks.data.load_dataset import HashedStudentData
import numpy as npy
import pickle
import os

class NearestStudents(Task):

    github_id = Parameter(default='b280302a', description='Github id to search nearby (not hashed)')
    n = IntParameter(default=5, description='Output top N')
    farthest = BoolParameter(default=False, description='Find farthest instead')
    
    def output(self):
        return luigi.LocalTarget("/Users/adcxdpf/Downloads/pset_03/sd.csv")
        

    def requires(self):
        return {
            'data': HashedStudentData(path='/Users/adcxdpf/Downloads/pset_03/pset/tasks/data'),
            'embedStudentData': EmbedStudentData(path='/Users/adcxdpf/Downloads/pset_03/pset/tasks/data')
         }
        #return self.clone(EmbedStudentData)


    def run(self):
        
        vectors_lookup_bytes = (self.input()['embedStudentData'].open(mode='rb'))
        vectors_lookup = pickle.load(vectors_lookup_bytes)

        vecs_list = pd.Series(vectors_lookup)
        vectors_df = pd.DataFrame(vectors_lookup, index=vecs_list.index)
        vectors_df.columns = ['vectors']
        print('##### vectors_df : ', vectors_df)
        print(" vectors_df shape is :: " , vectors_df.shape)
        
        print("github_id param : " , self.github_id)
                
        pd_xls_data = pd.read_excel(self.input()['data'].path,0)        
        idx = pd_xls_data.index[pd_xls_data['hashed_id']== self.github_id]
        #print ('######## idx.values ######### ', idx.values)
                
        my_vec = vectors_df.iloc[[idx.values[0]]]
        self.my_vec = (my_vec.values[0][0])
        
        print ("my_vec : " , self.my_vec)
        print(" my_vec shape is :: " , self.my_vec.shape)
        
        distances = vectors_df['vectors'].apply(self.my_distance)
        
        sortedDistance= distances.sort_values()
        print('###### sortedDistance : ', sortedDistance)
        
        # output data
        f = self.output().open('w')
        sortedDistance.str[0].to_csv(f)
        #df.to_csv(f, sep='\t', encoding='utf-8', index=None)
        f.close()        
        
        nearDis= sortedDistance.head(self.n).index
        print ("******** Nearest**********")
        for index in nearDis:            
            print(pd_xls_data.iloc[index])        
        
        farDis = sortedDistance.tail(5).index
        print ("******** Farthest**********")
        for index in farDis:            
            print(pd_xls_data.iloc[index])        
        


    def cosine_similarity(self,a, b):
    #     """Takes 2 vectors a, b and returns the cosine similarity according 
    #     to the definition of the dot product
    #     """
    #     dot_product = npy.dot(a, b)
    #     norm_a = npy.linalg.norm(a)
    #     norm_b = npy.linalg.norm(b)
    #     return dot_product / (norm_a * norm_b)
    
        
        dot_product = npy.dot(a[0], b.T)
        norm_a = npy.linalg.norm(a)
        norm_b = npy.linalg.norm(b)
        
        return dot_product / (norm_a * norm_b)
        

    def my_distance(self,vec1):
        
        return 1 - self.cosine_similarity(vec1, self.my_vec)
