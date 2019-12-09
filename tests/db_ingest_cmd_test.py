import filecmp, os, shutil, subprocess, tempfile, unittest
from click.testing import CliRunner

from .context import lah
from lah.db import LahDb
from lah.haplotig import Haplotig
from lah.chromosome import Chromosome
from lah.db_ingest_cmd import db_ingest_cmd

class LahDbIngestCliTests(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.dbfile = os.path.join(self.temp_dn, "test.db")
        self.out = tempfile.NamedTemporaryFile()
        self.err = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.temp_d.cleanup()

    def validate(self):
        self.assertTrue(os.path.exists(self.dbfile))
        LahDb.connect(self.dbfile)
        session =LahDb.session()

        chromosome = session.query(Chromosome).filter(Chromosome.name == "chr").first()
        self.assertIsNotNone(chromosome)
        self.assertEqual(chromosome.id, 1)

        haplotigs = session.query(Haplotig).all()
        self.assertTrue(len(haplotigs), 4)

    def test1_ingest(self):
        runner = CliRunner()

        result = runner.invoke(db_ingest_cmd, [])
        self.assertEqual(result.exit_code, 2)
        #result = runner.invoke(db_ingest_cmd, ["-h"]) 
        #self.assertEqual(result.exit_code, 0)
        result = runner.invoke(db_ingest_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        haplotigs_bn = "chr.haplotigs.tsv"
        haplotigs_source = os.path.join(self.data_d, haplotigs_bn)
        self.assertTrue(os.path.exists(haplotigs_source))
        haplotigs_fn = os.path.join(self.temp_dn, haplotigs_bn)
        shutil.copyfile(os.path.join(self.data_d, haplotigs_bn), haplotigs_fn)

        result = runner.invoke(db_ingest_cmd, ["--chromosome-name", "chr", "--dbfile", self.dbfile, "-f", haplotigs_fn, "-g", "NA,rid,hid"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.validate()

# -- LahDbIngestCliTests

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
