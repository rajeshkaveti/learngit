from luigi import ExternalTask
from luigi import Task
import luigi
import os
import pandas as pd
import numpy as np

class HashedStudentData(ExternalTask):
    path = luigi.Parameter()
    
    def output(self):
        print("************Inside HashedStudentData**********")
        return luigi.LocalTarget(os.path.join(self.path, 'hashed.xlsx'))
        
        
class Words(ExternalTask):
    path = luigi.Parameter()
            
    def output(self):
        return luigi.LocalTarget(os.path.join(self.path, 'words.txt'))
        

class Vectors(ExternalTask):
    path = luigi.Parameter()
            
    def output(self):
        return luigi.LocalTarget(os.path.join(self.path, 'vectors.npy.gz') , format=luigi.format.Nop)     
        

class WordVectors(ExternalTask):

    def requires(self):
        # Note the clone method - avoid creating task instances directly
        return [
                self.clone(Words),
                self.clone(Vectors)
        ]        


    def load_embedding(self):
        """Convenience method to load a :class:`.WordEmbedding`"""

        word_target = self.input()
        vec_target = self.output()

        # Use these targets to return a WordEmbedding instance
        
class TestTask(Task):
    path = luigi.Parameter()
    
    def requires(self):
        print("*********path from command line ********: " , self.path)  
        return self.clone(Words)
    
    def run(self):
        # Placeholder
        
        df = pd.read_csv(self.input().open('r'), sep=',')
        
        print(df)