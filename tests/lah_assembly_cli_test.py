import filecmp, os, subprocess, tempfile, unittest

class LahAssemblyCliTest(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.TemporaryFile()
        self.err = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()
        self.err.close()
        if hasattr(self, "tempdir"):
            self.tempdir.cleanup()

    def test1_lah_assembly(self):
        rv = subprocess.call(["lah", "assembly"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

    def test2_lah_assembly_prepare(self):
        rv = subprocess.call(["lah", "assembly", "prepare"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "assembly", "prepare", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "prepare", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

        tempdir = tempfile.TemporaryDirectory()
        self.tempdir = tempdir
        data_d = os.path.join(os.path.dirname(__file__), "data", "lah_assembly")
        edge_map_fn = os.path.join(data_d, "hap3.edge-map.tsv")
        rv = subprocess.call(["lah", "assembly", "prepare", "--directory", str(tempdir), "--source", edge_map_fn], stdout=self.out)
        self.assertEqual(rv, 0)

        haplotype_d = os.path.join(str(tempdir), "hap3")
        self.assertTrue(os.path.exists(os.path.join(haplotype_d, "asm.sh")))
        self.assertTrue(filecmp.cmp(os.path.join(haplotype_d, "reads"), os.path.join(data_d, "reads")))

# -- LahAssemblyCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
