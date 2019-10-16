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

    def test2_lah_assembly_merge(self):
        rv = subprocess.call(["lah", "assembly", "merge"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "assembly", "merge", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "merge", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

        data_d = os.path.join(os.path.dirname(__file__), "data", "assembly")
        edge_map_fn = os.path.join(data_d, "edge-map.tsv")
        self.tempdir = tempfile.TemporaryDirectory()
        assembly_fa = os.path.join(self.tempdir.name, "assembly.fasta")

        rv = subprocess.call(["lah", "assembly", "merge", "--directory", data_d, "--source", edge_map_fn, "--output", assembly_fa], stdout=self.out)
        self.assertEqual(rv, 0)

        self.assertTrue(os.path.exists(assembly_fa))
        self.assertTrue(filecmp.cmp(assembly_fa, os.path.join(data_d, "expected.assembly.fasta")))

    def test3_lah_assembly_prepare(self):
        rv = subprocess.call(["lah", "assembly", "prepare"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "assembly", "prepare", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "prepare", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

        tempdir = tempfile.TemporaryDirectory()
        self.tempdir = tempdir
        data_d = os.path.join(os.path.dirname(__file__), "data", "haplotype")
        hid = "402_0_2_0"
        edge_map_fn = os.path.join(data_d, "{}.edge-map.tsv".format(hid))
        rv = subprocess.call(["lah", "assembly", "prepare", "--directory", tempdir.name, "--source", edge_map_fn], stdout=self.out)
        self.assertEqual(rv, 0)

        haplotype_d = os.path.join(tempdir.name, hid)
        self.assertTrue(os.path.exists(os.path.join(haplotype_d, "asm.sh")))
        self.assertTrue(filecmp.cmp(os.path.join(haplotype_d, "reads"), os.path.join(data_d, "{}.reads".format(hid))))

# -- LahAssemblyCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
