import subprocess, tempfile, unittest

class LahHaplotigsCliTest(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.TemporaryFile()
        self.err = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()
        self.err.close()

    def test1_lah_haplotigs(self):
        rv = subprocess.call(["lah", "haplotigs"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotigs", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotigs", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

    def test2_lah_haplotigs_list(self):
        rv = subprocess.call(["lah", "haplotigs", "list"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotigs", "list", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotigs", "list", "--help"], stdout=self.out)

    def test3_lah_haplotigs_reads(self):
        rv = subprocess.call(["lah", "haplotigs", "reads"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotigs", "reads", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotigs", "reads", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

    def test3_lah_haplotigs_generate_fastq(self):
        rv = subprocess.call(["lah", "haplotigs", "generate-fastq"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotigs", "generate-fastq", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotigs", "generate-fastq", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

# -- LahHaplotigsCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__