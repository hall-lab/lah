import os, unittest
from mock import patch

from lah.models import Haplotig
import lah.haplotig_iters

class LahHaplotigItersTest(unittest.TestCase):
    def setUp(self):
        self.haplotigs_fn = os.path.join(os.path.dirname(__file__), "data", "sample", "chr.haplotigs.tsv")
        self.haplotigs_headers = ["NA", "rid", "hid"]

    def test1_validate_headers(self):
        with self.assertRaisesRegex(Exception, "Missing required headers: rid"):
            lah.haplotig_iters.HaplotigIterator.validate_headers(["NA", "READ", "hid"])

    def test2_haplotig_iterator(self):
        in_fn = self.haplotigs_fn

        with self.assertRaisesRegex(Exception, "Missing required headers: rid"):
            lah.haplotig_iters.HaplotigIterator(headers=["NA", "READ", "hid"], in_fn=in_fn)

        haplotig_iter = lah.haplotig_iters.HaplotigIterator(headers=self.haplotigs_headers, in_fn=in_fn)
        self.assertIsNotNone(haplotig_iter)

        haplotigs = []
        for h in haplotig_iter:
            haplotigs.append(h)
        self.assertIsNone(haplotig_iter.previous_hap)
        self.assertEqual(len(haplotigs), 4)

        self.assertEqual(haplotigs[0]["hid"], "401_0_1_0")
        self.assertEqual(len(haplotigs[0]["rids"]), 1)
        self.assertEqual(haplotigs[1]["hid"], "401_0_2_0")
        self.assertEqual(len(haplotigs[1]["rids"]), 2)
        self.assertEqual(haplotigs[2]["hid"], "402_0_1_0")
        self.assertEqual(len(haplotigs[2]["rids"]), 8)
        self.assertEqual(haplotigs[3]["hid"], "402_0_2_0")
        self.assertEqual(len(haplotigs[3]["rids"]), 14)

        self.assertEqual(haplotigs[0]["file_pos"], 0)
        self.assertEqual(haplotigs[1]["file_pos"], 60)
        self.assertEqual(haplotigs[2]["file_pos"], 178)
        self.assertEqual(haplotigs[3]["file_pos"], 655)

    def test2_haplotig_iterator_with_pos(self):
        in_fn = self.haplotigs_fn

        with self.assertRaisesRegex(Exception, "Missing required headers: rid"):
            lah.haplotig_iters.HaplotigIterator(headers=["NA", "READ", "hid"], in_fn=in_fn)

        haplotig_iter = lah.haplotig_iters.HaplotigIterator(headers=self.haplotigs_headers, in_fn=in_fn, pos=178)
        self.assertIsNotNone(haplotig_iter)
        haplotig = next(haplotig_iter)
        self.assertEqual(haplotig["hid"], "402_0_1_0")
        self.assertEqual(len(haplotig["rids"]), 8)
        self.assertEqual(haplotig["file_pos"], 178)

    @patch("lah.models.Haplotig")
    def test3_load_haplotig_reads(self, Hap):
        haplotig = Hap()
        haplotig.name = "402_0_1_0"
        haplotig.file_pos = 178
        haplotig_iter = lah.haplotig_iters.HaplotigIterator(headers=self.haplotigs_headers, in_fn=self.haplotigs_fn)
        haplotig_iter.load_haplotig_reads(haplotig)
        expected_reads = [
            "m54238_180909_174539/15467504/ccs",
            "m54238_180909_174539/24445361/ccs",
            "m54238_180910_180559/31916502/ccs",
            "m54238_180914_183539/60817532/ccs",
            "m54238_180916_191625/17694942/ccs",
            "m54328_180924_001027/12976682/ccs",
            "m54335_180925_223313/49349181/ccs",
            "m54335_180926_225328/38011681/ccs",
        ]
        self.assertEqual(haplotig.reads, expected_reads)

# -- LahHaplotigItersTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
