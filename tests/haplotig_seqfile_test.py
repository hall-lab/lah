import filecmp, io, os, sys, tempfile, unittest
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

        db = LahDb(self.dbfile)
        sm = db.connect()
        session = sm()
        self.haplotig = session.query(Haplotig).get(3)
        self.assertIsNotNone(self.haplotig)
        self.output = self.haplotig.seqfile_fn(self.temp_dn)
        self.source_seqfiles = session.query(Seqfile).all()

    def tearDown(self):
        self.temp_d.cleanup()

    def test0_haplotig_seqfile_attrs(self):
        seqfile_bn = self.haplotig.seqfile_bn()
        self.assertEqual(seqfile_bn, ".".join([self.haplotig.name, "fastq"]))
        self.assertEqual(self.haplotig.seqfile_fn(self.temp_dn), os.path.join(self.temp_dn, seqfile_bn))

    def test1_haplotig_seqfile(self):
        with self.assertRaisesRegex(Exception, "No reads loaded for haplotig"):
            self.haplotig.seqfile(sources=self.source_seqfiles, output=self.output)

        sys.stdout = io.StringIO() # silence stdout
        self.haplotig.chromosome.load_haplotig(self.haplotig)
        self.haplotig.seqfile(sources=self.source_seqfiles, output=self.output)
        self.assertTrue(filecmp.cmp(self.output, os.path.join(self.data_d, "402_0_1_0.fastq")))
        sys.stdout = sys.__stdout__

    def test2_haplotig_seqfile_cmd(self):
        runner = CliRunner()

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, ["--hid", self.haplotig.id, "--dbfile", self.dbfile, "--output", self.output])
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
