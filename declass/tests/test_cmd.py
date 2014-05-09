import unittest
from StringIO import StringIO
import sys
from numpy.testing import assert_allclose
from datetime import datetime
import copy
from collections import Counter, OrderedDict

from declass.cmd import files_to_vw


class TestFilesToVW(unittest.TestCase):
    """
    """
    def setUp(self):
        self.outfile = StringIO()

    def test_tokenize_basic_01(self):
        path_list = ['data/file1.txt', 'data/file2.txt', 'data/file3']
        files_to_vw.tokenize(self.outfile, path_list=path_list,
            tokenizer_type='basic')
        result = self.outfile.getvalue()
        benchmark = (
            "'file1 | know:1 here:1 cat:1\n"
            "'file2 | here:1 elephant:1\n"
            "'file3 | this'ssss:1\n")
        self.assertEqual(result, benchmark)

    def tearDown(self):
        self.outfile.close()
