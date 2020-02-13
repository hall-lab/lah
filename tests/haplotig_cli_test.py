import subprocess, tempfile, unittest

class LahhaplotigCliTest(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.TemporaryFile()
        self.err = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()
        self.err.close()

    def test1_lah_haplotig(self):
        rv = subprocess.call(["lah", "haplotig"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotig", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotig", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

    def test2_lah_haplotig_list(self):
        rv = subprocess.call(["lah", "haplotig", "list"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotig", "list", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotig", "list", "--help"], stdout=self.out)

    def test3_lah_haplotig_reads(self):
        rv = subprocess.call(["lah", "haplotig", "reads"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotig", "reads", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotig", "reads", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

    def test3_lah_haplotig_generate_fastq(self):
        rv = subprocess.call(["lah", "haplotig", "seqfile"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotig", "seqfile", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotig", "seqfile", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

# -- LahhaplotigCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
