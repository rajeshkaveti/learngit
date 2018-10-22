import luigi
import os

class Requirement:
    def __init__(self,  task_class , **params):
        self.task_class = task_class
        print("self.task_class : " , self.task_class)
        self.params = params

    def __get__(self, task, cls):
        task = self.task_class()

        return task.clone(self.task_class, **self.params)


class WordsTask(luigi.ExternalTask):
    def output(self):
        return luigi.LocalTarget(os.path.join('data/words.txt'))


class Requires:

    def __get__(self, task, cls):
        # Bind self/task in a closure
        self.task = WordsTask
        return lambda: self(task)

    def __call__(self, task):
        """Returns the requirements of a task"""
        print("__call__ called")

        if (isinstance(self.task(), WordsTask)):
            return {'other': self.task()}
        else:
            return None

class MyTask(luigi.Task):
    requires = Requires()

    other = Requirement(WordsTask)

    print("wordstask :: " , other)


    def run(self):
        with self.other.output().open('r') as wordsfile:
            mywords = wordsfile.readlines()
            print('mywords :: ', mywords)

if __name__ == '__main__':
    #mytask = MyTask()
    #print(mytask.requires())

    luigi.build([MyTask()], local_scheduler=True)

