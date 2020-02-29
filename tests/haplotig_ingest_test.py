import os, shutil, tempfile, unittest
from click.testing import CliRunner

from lah.db import LahDb
from lah.models import *
from lah.cli import cli
from lah.haplotig_ingest import haplotig_ingest_cmd as cmd

class LahDbIngestCliTests(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "dataset")
        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.dbfile = os.path.join(self.temp_dn, "test.db")

    def tearDown(self):
        self.temp_d.cleanup()

    def validate(self):
        self.assertTrue(os.path.exists(self.dbfile))
        db = LahDb(dbfile=self.dbfile)
        db.connect()
        session = db.session()

        metadata = session.query(Metadata).all()
        self.assertTrue(len(metadata), 3)

        haplotigs = session.query(Haplotig).all()
        self.assertTrue(len(haplotigs), 4)

        session.close()

    def test1_ingest(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["-d", self.dbfile, "db", "ingest"])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        haplotigs_bn = "haplotigs.tsv"
        haplotigs_source = os.path.join(self.data_d, haplotigs_bn)
        self.assertTrue(os.path.exists(haplotigs_source))
        haplotigs_fn = os.path.join(self.temp_dn, haplotigs_bn)
        shutil.copyfile(os.path.join(self.data_d, haplotigs_bn), haplotigs_fn)

        LahDb(self.dbfile).create()
        result = runner.invoke(cli, ["-d", self.dbfile, "haplotig", "ingest", "-f", haplotigs_fn, "-g", "NA,rid,hid"])
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
