import luigi
import pandas as pd
from load_dataset import *
from luigi.task import flatten
from hashlib import sha256


def get_salted_version(task):
    """Create a salted id/version for this task and lineage
    :returns: a unique, deterministic hexdigest for this task
    :rtype: str
    """
    msg = ""
    # Uniquely specify this task
    msg += ','.join([

            # Basic capture of input type
            task.__class__.__name__,

            # Change __version__ at class level when everything needs rerunning!
            task.__version__,

        ]
    )
    return sha256(msg.encode()).hexdigest()

class SaltedOutput:
    __version__ = '1.0'

    def __init__(self, base_dir='data', file_pattern='{task.__class__.__name__}-{hash}',ext='.txt',  **target_kwargs):
        self.base_dir = base_dir
        self.ext = ext

    def __get__(self, task, cls):
        # Determine the path etc here

        self.file_pattern = '{task.__name__}-{hash}'.format(task=cls, hash=get_salted_version(cls)[:6])
        self.path = self.base_dir + '/' + self.file_pattern + self.ext

        return lambda: luigi.LocalTarget(self.path)


class MyTask(Task):
    # Compose output
    __version__ = '1.0'
    output = SaltedOutput()

    def run(self):
        with self.output().open('w') as wordsfile:
            wordsfile.write("Hi!")


if __name__ == '__main__':
    mytask = MyTask()
    luigi.build([mytask], local_scheduler=True)
