import subprocess, tempfile, unittest

class LahReadGroupsCliTest(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.TemporaryFile()
        self.err = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()
        self.err.close()

    def test1_lah_read_groups(self):
        rv = subprocess.call(["lah", "read-groups"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "read-groups", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "read-groups", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

    def test2_lah_read_groups_list(self):
        rv = subprocess.call(["lah", "read-groups", "list"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "read-groups", "list", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "read-groups", "list", "--help"], stdout=self.out)

    def test3_lah_read_groups_reads(self):
        rv = subprocess.call(["lah", "read-groups", "reads"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "read-groups", "reads", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "read-groups", "reads", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

    def test3_lah_read_groups_generate_fastq(self):
        rv = subprocess.call(["lah", "read-groups", "generate-fastq"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "read-groups", "generate-fastq", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "read-groups", "generate-fastq", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

# -- LahReadGroupsCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
