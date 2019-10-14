import subprocess, tempfile, unittest

class SxDedupCliTest(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.TemporaryFile()
        self.err = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()
        self.err.close()

    def test1_sx_dedup_cli(self):
        rv = subprocess.call(['sx', 'dedup'], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)

    def test2_sx_dedup_by_name_cli(self):
        rv = subprocess.call(['sx', 'dedup', 'by-name', '--help'], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)
        rv = subprocess.call(['sx', 'dedup', 'by-name'], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)

# -- SxDedupCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
