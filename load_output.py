import luigi
import pandas as pd
from load_dataset import *

class SaltedOutput:
    def __init__(self, base_dir='data', file_pattern='{task.__class__.__name__}-{hash}',ext='.txt', **target_kwargs):
        self.base_dir = base_dir
        self.file_pattern = file_pattern
        self.ext = ext

    def __get__(self, task, cls):
        # Determine the path etc here
        self.file_pattern = '{task.__class__.__name__}-{hash}'.format(task=cls(), hash='123')
        self.path = self.base_dir + '/' + self.file_pattern + self.ext

        print("path is : " , self.path)

        return lambda: luigi.LocalTarget(self.path)


class MyTask:
    # Compose output

    output = SaltedOutput()

if __name__ == '__main__':

    out = MyTask().output()

    print('out : ',out)

    with out.open('w') as f:
        f.write('Hello !')

