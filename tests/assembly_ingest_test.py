import filecmp, os, subprocess, tempfile, unittest

from .context import lah
from lah.assembly import Assembly
from lah.db import LahDb
from lah.haplotig import Haplotig

class LahAssemblyIngestTests(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "assembly")
        self.temp_d = tempfile.TemporaryDirectory()
        self.dbfile = os.path.join(self.temp_d.name, "test.db")
        self.out = tempfile.NamedTemporaryFile()
        self.err = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.temp_d.cleanup()

    def verify_assembly(self, session):
        self.assertTrue(os.path.exists(self.dbfile))

        assemblies = session.query(Assembly).all()
        self.assertEqual(len(assemblies), 1)
        self.assertEqual(assemblies[0].directory, self.temp_d.name)

        haplotigs = session.query(Haplotig).all()
        self.assertTrue(len(haplotigs), 4)

    def test_assembly_ingest(self):
        db = lah.db.LahDb(dbfile=self.dbfile)
        db.create()
        sessionmaker = db.connect()
        session = sessionmaker()

        haplotigs_fn = os.path.join(self.data_d, "edge-map.tsv")
        assembly = Assembly(directory=self.temp_d.name)
        session.add(assembly)
        assembly.ingest(session=session, haplotigs_fn=haplotigs_fn)
        session.commit()

        self.verify_assembly(session)

    def test2_assembly_ingest_cli(self):
        rv = subprocess.call(["lah", "assembly", "ingest"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "assembly", "ingest", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "ingest", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

        haplotigs_fn = os.path.join(self.data_d, "edge-map.tsv")
        rv = subprocess.call(["lah", "assembly", "ingest", "--asm-dir", self.temp_d.name, "--dbfile", self.dbfile, "--read-groups", haplotigs_fn], stdout=self.out)
        self.assertEqual(rv, 0)

        db = LahDb(dbfile=self.dbfile)
        sessionmaker = db.connect()
        self.verify_assembly(sessionmaker())

# -- LahAssemblyIngestTests

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
