import filecmp, os, shutil, subprocess, tempfile, unittest

from .context import lah
from lah.assembly import Assembly
from lah.haplotig import Haplotig
from lah.db import LahDb

class LahAssemblyMergeTests(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "assembly")
        self.temp_d = tempfile.TemporaryDirectory()
        self.assembly_d = os.path.join(self.temp_d.name, "asm")
        shutil.copytree(self.data_d, self.assembly_d)
        self.out = tempfile.NamedTemporaryFile()
        self.err = tempfile.NamedTemporaryFile()

        dbfile = os.path.join(self.assembly_d, "test.db")
        shutil.copyfile(os.path.join(self.data_d, "test.db"), dbfile)

        db = LahDb(dbfile=dbfile)
        sessionmaker = db.connect()
        session = sessionmaker()
        assembly = session.query(Assembly).first()
        assembly.directory = self.assembly_d
        session.commit()

        os.remove(assembly.merged_fasta())

        self.assembly = assembly
        self.dbfile = dbfile
        self.session = session

    def tearDown(self):
        self.temp_d.cleanup()
        self.out.close()
        self.err.close()

    def verify_merged_fasta(self):
        assembly_fa = self.assembly.merged_fasta()
        self.assertTrue(os.path.exists(assembly_fa))
        self.assertTrue(filecmp.cmp(assembly_fa, os.path.join(self.data_d, "assembly.fasta")))

    def test_assembly_merge(self):
        metrics = self.assembly.merge(self.session)
        self.assertEqual(metrics, {"skipped one read": 1, "skipped no assembly": 0, "count": 3})
        self.verify_merged_fasta()

    def test_assembly_merge_cli(self):
        rv = subprocess.call(["lah", "assembly", "merge"], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 2)
        rv = subprocess.call(["lah", "assembly", "merge", "-h"], stdout=self.out)
        self.assertEqual(rv, 0)
        rv = subprocess.call(["lah", "assembly", "merge", "--help"], stdout=self.out)
        self.assertEqual(rv, 0)

        rv = subprocess.call(["lah", "assembly", "merge", "--dbfile", self.dbfile], stdout=self.out, stderr=self.err)
        self.assertEqual(rv, 0)

        self.verify_merged_fasta()

# -- LahAssemblyMergeTests

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
