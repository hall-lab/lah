import subprocess, tempfile, unittest

class SxSubsetCliTest(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.TemporaryFile()
        self.err = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()
        self.err.close()

    def test1_sx_subset_cli(self):
        rv = subprocess.call(['sx', 'subset'], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)

    def test2_sx_subset_by_name_cli(self):
        rv = subprocess.call(['sx', 'subset', 'by-name', '--help'], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)
        rv = subprocess.call(['sx', 'subset', 'by-name'], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)

# -- SxSubsetCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
