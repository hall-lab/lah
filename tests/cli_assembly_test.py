import filecmp, os, subprocess, tempfile, unittest

class LahAssemblyCliTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "assembly")
        self.temp_d = tempfile.TemporaryDirectory()
        self.out = tempfile.NamedTemporaryFile()
        self.err = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.out.close()
        self.err.close()
        self.temp_d.cleanup()

    def test1_lah_assembly(self):
        rv = subprocess.call(["lah", "assembly"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

# -- LahAssemblyCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
