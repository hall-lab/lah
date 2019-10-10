import subprocess, tempfile, unittest

class LahCliTest(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()

    def test1_sx(self):
        rv = subprocess.call(['lah'], stdout=self.out)
        self.assertEqual(rv, 0)

# -- LahCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
