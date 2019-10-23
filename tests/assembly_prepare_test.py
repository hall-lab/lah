import filecmp, os, shutil, subprocess, tempfile, unittest

from .context import lah
from lah.assembly import Assembly
from lah.haplotype import Haplotype
from lah.db import LahDb

class LahAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "assembly")
        self.temp_d = tempfile.TemporaryDirectory()
        self.out = tempfile.NamedTemporaryFile()
        self.err = tempfile.NamedTemporaryFile()

        dbfile = os.path.join(self.temp_d.name, "test.db")
        shutil.copyfile(os.path.join(self.data_d, "test.db"), dbfile)

        db = LahDb(dbfile=dbfile)
        sessionmaker = db.connect()
        session = sessionmaker()
        assembly = session.query(Assembly).first()
        assembly.directory = self.temp_d.name
        session.commit()

        self.assembly = assembly
        self.dbfile = dbfile
        self.session = session

    def tearDown(self):
        self.temp_d.cleanup()
        self.out.close()
        self.err.close()

    def verify_assembly(self):
        self.assertTrue(os.path.exists(self.dbfile))
        haplotypes_d = os.path.join(self.temp_d.name, "haplotypes")
        self.assertTrue(os.path.exists(haplotypes_d))
        for haplotype in self.session.query(Haplotype).all():
            haplotype_d = os.path.join(haplotypes_d, haplotype.name)
            self.assertTrue(os.path.exists(haplotype_d))
            self.assertTrue(os.path.exists( os.path.join(haplotype_d, "asm.sh") ))

    def test_assembly_prepare(self):
        self.assembly.prepare(self.session)
        self.verify_assembly()

    def test_assembly_prepare_cli(self):
        rv = subprocess.call(["lah", "assembly", "prepare"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "assembly", "prepare", "-h"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "prepare", "--help"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)

        rv = subprocess.call(["lah", "assembly", "prepare", "--dbfile", self.dbfile], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)
        self.verify_assembly()

# -- LahAssemblyTests

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
