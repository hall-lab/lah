import filecmp, os, shutil, tempfile, unittest

from .context import sx
import sx.io

class SxIoTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join( os.path.dirname(__file__), "data", "io")

    def tearDown(self):
        if hasattr(self, "temp_d"):
            self.temp_d.cleanup()

    def test1_type_for_file(self):
        with self.assertRaisesRegex(Exception, "Cannot determine sequence type from file: blah"):
            sx.io.type_for_file("blah")
        with self.assertRaisesRegex(Exception, "Unknown sequence file extension: \.blah"):
            sx.io.type_for_file("file.blah")
        for ext in (".fastq", ".fq"):
            self.assertEqual(sx.io.type_for_file("file"+ext), "fastq")
        for ext in (".fasta", ".fna", ".fa"):
            self.assertEqual(sx.io.type_for_file("file"+ext), "fasta")

    def test2_reader_writer(self):
        in_fastq_fn = os.path.join(self.data_d, "in.fastq")
        reader = sx.io.SxReader(seq_fn=in_fastq_fn)
        self.assertEqual(reader.seq_type, "fastq")
        seqs = []
        for seq in reader:
            seqs.append(seq)
        self.assertEqual(len(seqs), 4)

        reader.create_index()
        self.assertIsNotNone(reader.index)
        seq_from_index = reader.getseq(seqs[1].id)
        self.assertEqual(seq_from_index.seq, seqs[1].seq)

        seq_from_index = reader.getseq("blah")
        self.assertIsNone(seq_from_index)

        self.temp_d = tempfile.TemporaryDirectory()
        out_fasta_fn = os.path.join(self.temp_d.name, "out.fasta")
        writer = sx.io.SxWriter(seq_fn=out_fasta_fn)
        self.assertEqual(writer.seq_type, "fasta")
        writer.write(seqs=seqs[1::2])
        writer.flush()
        expected_fasta_fn = os.path.join(self.data_d, "out.fasta")
        self.assertTrue(filecmp.cmp(out_fasta_fn, expected_fasta_fn))

# -- SxIoTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
