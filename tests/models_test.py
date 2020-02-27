import os, unittest

from lah.db import LahDb
from lah.models import *

class ModelsTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "dataset")
        self.dbfile = os.path.join(self.data_d, "test.db")
        self.db = LahDb(self.dbfile)
        self.db.connect()

    def test_haplotig(self):
        session = self.db.session()
        haplotig = session.query(Haplotig).get(3)
        self.assertIsNotNone(haplotig)
        self.assertEqual(Haplotig.merged_bn(), "merged.fasta")
        self.assertEqual(Haplotig.merged_fn(self.data_d), os.path.join(self.data_d, "merged.fasta"))
        self.assertEqual(Haplotig.asm_files_sdn(), "asm-files")
        self.assertEqual(Haplotig.asm_sdn(), "assemblies")
        self.assertEqual(haplotig.asm_fn(self.data_d), os.path.join(self.data_d, "assemblies", ".".join([haplotig.name, "contigs", "fasta"])))
        self.assertEqual(Haplotig.seqfile_sdn(), "haplotigs")
        self.assertEqual(haplotig.seqfile_fn(self.data_d), os.path.join(self.data_d, "haplotigs", ".".join([haplotig.name, "fastq"])))

    def test_metadata(self):
        session = self.db.session()
        md = session.query(Metadata).all()
        self.assertEqual(len(md), 3)

    def test_metrics(self):
        session = self.db.session()
        metrics = session.query(Metric).all()
        self.assertEqual(len(metrics), 2)

    def test_seqfiles(self):
        session = self.db.session()
        seqfile = session.query(Seqfile).first()
        self.assertIsNotNone(seqfile)
        self.assertEqual(seqfile.idx_fn(), ".".join([seqfile.fn, "fai"]))

# -- ModelsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
