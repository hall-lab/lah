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

    def test3_lah_assembly_merge(self):
        rv = subprocess.call(["lah", "assembly", "merge"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "assembly", "merge", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "merge", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

        data_d = os.path.join(os.path.dirname(__file__), "data", "assembly")
        edge_map_fn = os.path.join(data_d, "edge-map.tsv")
        assembly_fa = os.path.join(self.temp_d.name, "assembly.fasta")

        rv = subprocess.call(["lah", "assembly", "merge", "--directory", data_d, "--source", edge_map_fn, "--output", assembly_fa], stdout=self.out)
        self.assertEqual(rv, 0)

        self.assertTrue(os.path.exists(assembly_fa))
        self.assertTrue(filecmp.cmp(assembly_fa, os.path.join(data_d, "expected.assembly.fasta")))

# -- LahAssemblyCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
