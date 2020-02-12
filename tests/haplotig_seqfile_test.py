import filecmp, io, os, sys, tempfile, unittest
from click.testing import CliRunner

from lah.cli import cli
from lah.haplotig import Haplotig, Metadata
from lah.haplotig_iters import HaplotigIterator
from lah.db import LahDb
from lah.seqfiles import Seqfile
from lah.haplotig_seqfile_cmd import haplotig_seqfile_cmd as cmd

class HaplotigSeqfileCmdTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        self.haplotigs_dn = os.path.join(self.data_d, "haplotigs")
        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name

        db = LahDb(self.dbfile)
        db.connect()
        session = db.session()
        haplotigs_bn = session.query(Metadata).filter_by(name="haplotigs_fn").one().value
        self.haplotigs_fn = os.path.join(self.data_d, haplotigs_bn)
        self.haplotigs_headers = session.query(Metadata).filter_by(name="haplotigs_headers").one().value.split(",")
        self.haplotig = session.query(Haplotig).get(3)
        self.output = self.haplotig.seqfile_fn(self.temp_dn)
        self.source_seqfiles = session.query(Seqfile).all()

    def tearDown(self):
        self.temp_d.cleanup()

    def test0_haplotig_seqfile_attrs(self):
        haplotig = self.haplotig
        self.assertIsNotNone(haplotig)
        seqfile_bn = haplotig.seqfile_bn()
        self.assertEqual(seqfile_bn, ".".join([haplotig.name, "fastq"]))
        self.assertEqual(haplotig.seqfile_fn(self.temp_dn), os.path.join(self.temp_dn, seqfile_bn))

    def test1_haplotig_seqfile(self):
        haplotig = self.haplotig
        self.assertIsNotNone(haplotig)
        with self.assertRaisesRegex(Exception, "No reads loaded for haplotig"):
            haplotig.seqfile(sources=self.source_seqfiles, output=self.output)

        sys.stdout = io.StringIO() # silence stdout

        haplotig_iter = HaplotigIterator(headers=self.haplotigs_headers, in_fn=self.haplotigs_fn)
        haplotig_iter.load_haplotig_reads(haplotig)

        haplotig.seqfile(sources=self.source_seqfiles, output=self.output)
        self.assertTrue(filecmp.cmp(self.output, os.path.join(self.haplotigs_dn, "402_0_1_0.fastq")))
        sys.stdout = sys.__stdout__

    def test2_haplotig_seqfile_cmd(self):
        runner = CliRunner()

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-d", self.dbfile, "haplotig", "seqfile", "--hid", self.haplotig.id, "--output", self.output])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertTrue(filecmp.cmp(self.output, os.path.join(self.haplotigs_dn, "402_0_1_0.fastq")))

# -- HaplotigSeqfileCmdTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
