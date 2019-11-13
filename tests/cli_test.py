import subprocess, tempfile, unittest

class SxCliTest(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()

    def test_lah(self):
        rv = subprocess.call(['lah'], stdout=self.out)
        self.assertEqual(rv, 0)

    def test_sx(self):
        rv = subprocess.call(['sx'], stdout=self.out)
        self.assertEqual(rv, 0)

# -- SxCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
