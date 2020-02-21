import filecmp, io, os, sys, tempfile, unittest
from click.testing import CliRunner

from lah.cli import cli
from lah.db import LahDb
from lah.models import *
from lah.haplotig_iters import HaplotigIterator
from lah.haplotig_seqfile import haplotig_seqfile_cmd, create_seqfile

class HaplotigSeqfileCmdTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        self.haplotigs_dn = os.path.join(self.data_d, "haplotigs")
        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.temp_dn = "tmp"

        db = LahDb(self.dbfile)
        db.connect()
        session = db.session()
        haplotigs_bn = session.query(Metadata).filter_by(name="haplotigs_fn").one().value
        self.haplotigs_fn = os.path.join(self.data_d, haplotigs_bn)
        self.haplotigs_headers = session.query(Metadata).filter_by(name="haplotigs_headers").one().value.split(",")
        self.haplotig = session.query(Haplotig).get(3)
        self.source_seqfiles = session.query(Seqfile).all()
        session.close()

    def tearDown(self):
        self.temp_d.cleanup()

    def test0_haplotig_seqfile_attrs(self):
        haplotig = self.haplotig
        self.assertIsNotNone(haplotig)
        seqfile_bn = haplotig.seqfile_bn()
        self.assertEqual(seqfile_bn, ".".join([haplotig.name, "fastq"]))
        self.assertEqual(haplotig.seqfile_fn(self.temp_dn), os.path.join(self.temp_dn, "haplotigs", seqfile_bn))

    def test1_create_seqfile(self):
        haplotig = self.haplotig
        self.assertIsNotNone(haplotig)
        output_fn = os.path.join(self.temp_dn, "seqfile.fastq")
        with self.assertRaisesRegex(Exception, "No reads loaded for haplotig"):
            create_seqfile(self.haplotig, sources=self.source_seqfiles, output=output_fn)

        sys.stdout = io.StringIO() # silence stdout

        haplotig_iter = HaplotigIterator(headers=self.haplotigs_headers, in_fn=self.haplotigs_fn)
        haplotig_iter.load_haplotig_reads(haplotig)

        create_seqfile(self.haplotig, sources=self.source_seqfiles, output=output_fn)
        self.assertTrue(filecmp.cmp(output_fn, os.path.join(self.haplotigs_dn, "402_0_1_0.fastq")))
        sys.stdout = sys.__stdout__

    def test2_haplotig_seqfile_cmd(self):
        runner = CliRunner()

        result = runner.invoke(haplotig_seqfile_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(haplotig_seqfile_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        output_fn = os.path.join(self.temp_dn, "from_cmd.fastq")
        result = runner.invoke(cli, ["-d", self.dbfile, "haplotig", "seqfile", str(self.haplotig.id), "--output", output_fn])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertTrue(filecmp.cmp(output_fn, os.path.join(self.haplotigs_dn, "402_0_1_0.fastq")))

# -- HaplotigSeqfileCmdTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
