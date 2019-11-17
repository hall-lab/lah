import filecmp, os, tempfile, unittest
from click.testing import CliRunner

from .context import lah
from lah.db import LahDb
from lah.chromosome import Chromosome
from lah.haplotig import Haplotig
from lah.seqfiles import Seqfile
from lah.haplotig_seqfile_cmd import haplotig_seqfile_cmd as cmd

class HaplotigSeqfileCmdTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.hid = 3
        self.h_name = "402_0_1_0"
        self.output = os.path.join(self.temp_dn, ".".join([self.h_name, "fastq"]))

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_haplotig_seqfile(self):
        db = LahDb(self.dbfile)
        sm = db.connect()
        session = sm()
        haplotig = session.query(Haplotig).get(self.hid)
        self.assertIsNotNone(haplotig)

        haplotig.chromosome.load_haplotig(haplotig)
        source_seqfiles = session.query(Seqfile).all()
        haplotig.seqfile(sources=source_seqfiles, output=self.output)
        self.assertTrue(filecmp.cmp(self.output, os.path.join(self.data_d, "402_0_1_0.fastq")))

    def test2_haplotig_seqfile_cmd(self):
        runner = CliRunner()

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, ["--hid", self.hid, "--dbfile", self.dbfile, "--output", self.output])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertTrue(filecmp.cmp(self.output, os.path.join(self.data_d, "402_0_1_0.fastq")))

# -- HaplotigSeqfileCmdTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
