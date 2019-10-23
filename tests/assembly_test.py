import os, tempfile, unittest

from .context import lah
from lah.assembly import Assembly
from lah.haplotype import Haplotype
import lah.db

class LahAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "assembly")
        self.temp_d = tempfile.TemporaryDirectory()
        self.dbfile = os.path.join(self.temp_d.name, "test.db")

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_assembly(self):
        dbfile = self.dbfile
        db = lah.db.LahDb(dbfile=dbfile)
        db.create()
        sessionmaker = db.connect()
        session = sessionmaker()

        asm = Assembly(directory="/blah")
        self.assertIsNotNone(asm)
        self.assertEqual(asm.directory, "/blah")

        session.add(asm)
        session.commit()
        self.assertEqual(asm.id, 1)
        asm = session.query(Assembly).first()
        self.assertEqual(asm.id, 1)

    def test2_assembly_createdb(self):
        db = lah.db.LahDb(dbfile=self.dbfile)
        db.create()
        sessionmaker = db.connect()
        session = sessionmaker()

        haplotypes_fn = os.path.join(self.data_d, "edge-map.tsv")
        lah.assembly.ingest(session=session, asm_dir=self.temp_d.name, haplotypes_fn=haplotypes_fn)
        session.commit()

        session = sessionmaker()
        haplotypes = session.query(Haplotype).all()
        self.assertTrue(len(haplotypes), 4)

# -- LahAssemblyTests

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
