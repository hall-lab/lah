import os, tempfile, unittest

from .context import lah
from lah.sample import Sample
from lah.haplotig import Haplotig
import lah.db

class LahSampleTests(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        self.dbfile = os.path.join(self.temp_d.name, "test.db")

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_sample(self):
        dbfile = self.dbfile
        db = lah.db.LahDb(dbfile=dbfile)
        db.create()
        sessionmaker = db.connect()
        session = sessionmaker()

        sample = Sample(name="McTesterson", directory="/blah")
        self.assertIsNotNone(sample)
        self.assertEqual(sample.directory, "/blah")

        session.add(sample)
        session.commit()
        self.assertEqual(sample.id, 1)
        sample = session.query(Sample).first()
        self.assertEqual(sample.id, 1)

        self.assertEqual(sample.merged_fasta(), "/blah/sample.fasta")

# -- LahSampleTests

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
