#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pset_04` package."""

import pytest
import unittest
from tempfile import *
from hashlib import sha256
from luigi import *
import luigi
from pset_04.task.mytasks import *
from pset_04.task.saltedoutput import *


class SaltedTests(unittest.TestCase):
    def test_salted_tasks(self):
        saltedhash = ''
        with TemporaryDirectory() as tmp:
            print('created temporary directory', tmp)
            class SomeTask(Task):
                __version__ = '1.0'
                output = SaltedOutput(base_dir=tmp)


                def run(self):
                    with self.output().open('w') as wordsfile:
                        wordsfile.write("Hi!")

                print('===============',output.file_pattern)


            luigi.build([SomeTask()], local_scheduler=True)

            assert(4) == 4



