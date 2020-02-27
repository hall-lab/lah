import filecmp, io, os, sys, unittest
from click.testing import CliRunner

from tests.dataset import Dataset
from lah.cli import cli
from lah.db import LahDb
from lah.models import *
from lah.haplotig_iters import HaplotigIterator
from lah.haplotig_seqfile import haplotig_seqfile_cmd, create_seqfile

class HaplotigSeqfileCmdTest(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset()

    def test0_haplotig_seqfile_attrs(self):
        db = LahDb(self.dataset.dbfile)
        db.connect()
        session = db.session()
        haplotig = session.query(Haplotig).get(3)
        self.assertIsNotNone(haplotig)
        seqfile_bn = haplotig.seqfile_bn()
        self.assertEqual(seqfile_bn, ".".join([haplotig.name, "fastq"]))
        self.assertEqual(haplotig.seqfile_fn(self.dataset.dn), os.path.join(self.dataset.dn, "haplotigs", seqfile_bn))
        session.close()
        db.disconnect()

    def test1_create_seqfile(self):
        db = LahDb(self.dataset.dbfile)
        db.connect()
        session = db.session()
        haplotig = session.query(Haplotig).get(3)
        self.assertIsNotNone(haplotig)
        seqfiles = session.query(Seqfile).all()
        self.assertEqual(len(seqfiles), 2)
        headers = session.query(Metadata).filter_by(name="haplotig_headers").one().value
        haplotigs_fn = session.query(Metadata).filter_by(name="haplotigs_fn").one().value

        output_fn = os.path.join(self.dataset.dn, "seqfile.fastq")
        with self.assertRaisesRegex(Exception, "No reads loaded for haplotig"):
            create_seqfile(haplotig, sources=seqfiles, output=output_fn)

        sys.stdout = io.StringIO() # silence stdout

        haplotig_iter = HaplotigIterator(headers=headers.split(","), in_fn=haplotigs_fn)
        haplotig_iter.load_haplotig_reads(haplotig)

        create_seqfile(haplotig, sources=seqfiles, output=output_fn)
        self.assertTrue(filecmp.cmp(output_fn, haplotig.seqfile_fn(self.dataset.data_dn)))
        sys.stdout = sys.__stdout__

    def test2_haplotig_seqfile_cmd(self):
        runner = CliRunner()

        result = runner.invoke(haplotig_seqfile_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(haplotig_seqfile_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        output_fn = os.path.join(self.dataset.dn, "from_cmd.fastq")
        result = runner.invoke(cli, ["-d", self.dataset.dbfile, "haplotig", "seqfile", "3", "--output", output_fn])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertTrue(filecmp.cmp(output_fn, os.path.join(self.dataset.data_dn, "haplotigs", "402_0_1_0.fastq")))

# -- HaplotigSeqfileCmdTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
