import subprocess, tempfile, unittest

class LahHaplotypesCliTest(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.TemporaryFile()
        self.err = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()
        self.err.close()

    def test1_lah_haplotypes(self):
        rv = subprocess.call(["lah", "haplotypes"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotypes", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotypes", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

    def test2_lah_haplotypes_list(self):
        rv = subprocess.call(["lah", "haplotypes", "list"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotypes", "list", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotypes", "list", "--help"], stdout=self.out)

    def test3_lah_haplotypes_reads(self):
        rv = subprocess.call(["lah", "haplotypes", "reads"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotypes", "reads", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotypes", "reads", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

    def test3_lah_haplotypes_generate_fastq(self):
        rv = subprocess.call(["lah", "haplotypes", "generate-fastq"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotypes", "generate-fastq", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotypes", "generate-fastq", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

# -- LahHaplotypesCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
