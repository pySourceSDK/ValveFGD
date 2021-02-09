import shutil
import tempfile
import os
import unittest
from valvefgd import FgdParse, FgdWrite


class WriteTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.fgd_file = os.path.join(self.test_dir, 'test.fgd')
        self.fgd = FgdParse('tests/fgds/tf/tf.fgd')
        self.basefgd = self.fgd.includes[0]
        return

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        return

    def test_writer(self):

        FgdWrite(self.fgd, self.fgd_file)
        with open(self.fgd_file, 'r') as file:
            text_result = file.read()

        self.assertEqual(text_result, self.fgd.fgd_str())

    def test_writer_collapse(self):

        FgdWrite(self.fgd, self.fgd_file, collapse=True)

        with open(self.fgd_file, 'r') as file:
            text_result = file.read()

        self.assertEqual(text_result, self.fgd.fgd_str(collapse=True))

    def test_writer_base(self):
        FgdWrite(self.basefgd, self.fgd_file)

        with open(self.fgd_file, 'r') as file:
            text_result = file.read()

        self.assertEqual(text_result, self.basefgd.fgd_str())
