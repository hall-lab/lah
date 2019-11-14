import filecmp, os, subprocess, tempfile, unittest

from .context import lah
from lah.db import LahDb
from lah.haplotig import Haplotig
from lah.sample import Sample
from lah.haplotig_iters import HaplotigIterator

class LahDbIngestTests(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.temp_d = tempfile.TemporaryDirectory()
        self.dbfile = os.path.join(self.temp_d.name, "test.db")
        self.out = tempfile.NamedTemporaryFile()
        self.err = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.temp_d.cleanup()

    def verify_sample(self, session):
        self.assertTrue(os.path.exists(self.dbfile))

        assemblies = session.query(Sample).all()
        self.assertEqual(len(assemblies), 1)
        self.assertEqual(assemblies[0].directory, self.temp_d.name)

        haplotigs = session.query(Haplotig).all()
        self.assertTrue(len(haplotigs), 4)

    def test1_sample_ingest(self):
        db = lah.db.LahDb(dbfile=self.dbfile)
        db.create()
        sessionmaker = db.connect()
        session = sessionmaker()

        haplotigs_fn = os.path.join(self.data_d, "edge-map.tsv")
        sample = Sample(name="McTesterson", directory=self.temp_d.name)
        session.add(sample)
        session.commit()
        haplotig_iter = HaplotigIterator(in_fn=haplotigs_fn, headers=["NA", "rid", "hid"])
        sample.ingest(session=session, haplotig_iter=haplotig_iter)
        session.commit()

        self.verify_sample(session)

    def test2_sample_ingest_cli(self):
        rv = subprocess.call(["lah", "db", "ingest"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "db", "ingest", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "db", "ingest", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

        haplotigs_fn = os.path.join(self.data_d, "edge-map.tsv")
        rv = subprocess.call(["lah", "db", "ingest", "--sample-name", "McTesterson", "--sample-dir", self.temp_d.name, "--dbfile", self.dbfile, "--haplotigs", haplotigs_fn, "-g", "NA,rid,hid"], stdout=self.out)
        self.assertEqual(rv, 0)

        db = LahDb(dbfile=self.dbfile)
        sessionmaker = db.connect()
        self.verify_sample(sessionmaker())

# -- LahDbIngestTests

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
