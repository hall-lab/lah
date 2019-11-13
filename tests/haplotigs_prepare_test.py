import filecmp, os, shutil, subprocess, tempfile, unittest

from .context import lah
from lah.sample import Sample
from lah.haplotig import Haplotig
from lah.db import LahDb

class LahHaplotigPrepareTests(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.temp_d = tempfile.TemporaryDirectory()
        self.sample_d = os.path.join(self.temp_d.name, "sample")
        self.out = tempfile.NamedTemporaryFile()
        self.err = tempfile.NamedTemporaryFile()

        os.makedirs(self.sample_d)
        dbfile = os.path.join(self.sample_d, "test.db")
        shutil.copyfile(os.path.join(self.data_d, "test.db"), dbfile)

        db = LahDb(dbfile=dbfile)
        sessionmaker = db.connect()
        session = sessionmaker()
        sample = session.query(Sample).first()
        sample.directory = self.sample_d
        session.commit()

        self.sample = sample
        self.dbfile = dbfile
        self.session = session

    def tearDown(self):
        self.temp_d.cleanup()
        self.out.close()
        self.err.close()

    def verify(self):
        self.assertTrue(os.path.exists(self.dbfile))
        self.assertTrue(os.path.exists(self.sample_d))
        for haplotig in self.session.query(Haplotig).all():
            haplotig_d = os.path.join(self.sample_d, "haplotigs", haplotig.name)
            self.assertTrue(os.path.exists(haplotig_d))
            self.assertTrue(os.path.exists( os.path.join(haplotig_d, "asm.sh") ))

    def test_haplotig_prepare(self):
        self.sample.prepare(self.session)
        self.verify()

    def test_haplotig_prepare_cli(self):
        rv = subprocess.call(["lah", "haplotigs", "prepare"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "haplotigs", "prepare", "-h"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "haplotigs", "prepare", "--help"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)

        rv = subprocess.call(["lah", "haplotigs", "prepare", "--dbfile", self.dbfile], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)

        self.verify()

# -- LahHaplotigPrepareTests

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
