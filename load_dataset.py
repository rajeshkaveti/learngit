from luigi import ExternalTask
from luigi import Task
import luigi
import os
from w_embedding import WordEmbedding

class HashedStudentData(ExternalTask):
    path = luigi.Parameter()
    
    def output(self):
        print("************Inside HashedStudentData**********")
        return luigi.LocalTarget(os.path.join(self.path, 'hashed.xlsx'))
        
        
class Words(ExternalTask):
    path = luigi.Parameter()
            
    def output(self):
        return luigi.LocalTarget(os.path.join(self.path, 'words.txt'))


class WordVectors(ExternalTask):
    path = luigi.Parameter()
    
    def requires(self):
        # Note the clone method - avoid creating task instances directly
        return self.clone(Words)
        
    def output(self):
        return luigi.LocalTarget(os.path.join(self.path, 'vectors.npy.gz') , format=luigi.format.Nop)
        
        
    def load_embedding(self):
        """Convenience method to load a :class:`.WordEmbedding`"""

        word_target = self.input()
        vec_target = self.output()
        
        return WordEmbedding(word_target,vec_target)

        # Use these targets to return a WordEmbedding instance
        
class TestTask(Task):
    path = luigi.Parameter()
    
    def requires(self):
        print("*********path from command line ********: " , self.path)  
        return self.clone(WordVectors)
    
    def run(self):
        # Placeholder
        pass
        
