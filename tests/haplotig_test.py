import os, tempfile, unittest

from .context import lah

class LahHaplotigTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test1(self):
        self.assertTrue(True)

# -- LahHaplotigTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
