import filecmp, os, subprocess, tempfile, unittest

class LahDbCliTest(unittest.TestCase):
    def setUp(self):
        self.data_d = data_d = os.path.join(os.path.dirname(__file__), "data", "db")
        self.out = tempfile.TemporaryFile()
        self.err = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()
        self.err.close()
        if hasattr(self, "tempdir"):
            self.tempdir.cleanup()

    def test1_lah_db(self):
        rv = subprocess.call(["lah", "db"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "db", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "db", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

    def test2_lah_db_create(self):
        rv = subprocess.call(["lah", "db", "create"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "db", "create", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "db", "create", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

        self.tempdir = tempfile.TemporaryDirectory()
        db_file = os.path.join(self.tempdir.name, "test.db")

        rv = subprocess.call(["lah", "db", "create", db_file], stdout=self.out)
        self.assertEqual(rv, 0)

        self.assertTrue(os.path.exists(db_file))
        self.assertTrue(os.path.getsize(db_file), 61440)

# -- LahDbCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
