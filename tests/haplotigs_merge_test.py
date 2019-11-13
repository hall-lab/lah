import filecmp, os, shutil, subprocess, tempfile, unittest

from .context import lah
from lah.sample import Sample
from lah.db import LahDb

class LahHaplotigMergeTests(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.temp_d = tempfile.TemporaryDirectory()
        self.sample_d = os.path.join(self.temp_d.name, "sample")
        shutil.copytree(self.data_d, self.sample_d)

        self.out = tempfile.NamedTemporaryFile()
        self.err = tempfile.NamedTemporaryFile()

        dbfile = os.path.join(self.sample_d, "test.db")
        db = LahDb(dbfile=dbfile)
        sessionmaker = db.connect()
        session = sessionmaker()
        sample = session.query(Sample).first()
        sample.directory = self.sample_d
        session.commit()

        os.remove(sample.merged_fasta())

        self.sample = sample
        self.dbfile = dbfile
        self.session = session

    def tearDown(self):
        self.temp_d.cleanup()
        self.out.close()
        self.err.close()

    def verify_merged_fasta(self):
        haplotig_fa = self.sample.merged_fasta()
        self.assertTrue(os.path.exists(haplotig_fa))
        self.assertTrue(filecmp.cmp(haplotig_fa, os.path.join(self.data_d, "sample.fasta")))

    def test_haplotig_merge(self):
        metrics = self.sample.merge(self.session)
        self.assertEqual(metrics, {"skipped one read": 1, "skipped no assembly": 0, "count": 3})
        self.verify_merged_fasta()

    def test_haplotig_merge_cli(self):
        rv = subprocess.call(["lah", "haplotigs", "merge"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotigs", "merge", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotigs", "merge", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

        rv = subprocess.call(["lah", "haplotigs", "merge", "--dbfile", self.dbfile], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)

        self.verify_merged_fasta()

# -- LahHaplotigMergeTests

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
