
import luigi
from luigi import *

class TaskA(luigi.Task):
    def requires(self):
        pass

    def output(self):
        return luigi.LocalTarget("data/abc.txt")


    def run(self):
        print("############ INSIDE TASK A RUN ################")
        with self.output().open('w') as f:
            f.write('Hello !')


class TaskB(luigi.Task):
    def requires(self):
        return {'a': TaskA()}

    def output(self):
        return luigi.LocalTarget("data/taskB.txt")

    def run(self):
        input = self.input()
        print("**************",  input)
