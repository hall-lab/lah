import os, unittest

from .context import lah
import lah.haplotig_iters

class LahHaplotigItersTest(unittest.TestCase):

    def test1_parse_line(self):
        rg = lah.haplotig_iters.HaplotigIterator.parse_line("ccs_31_21627397 @m54329_180927_232921/21627397/ccs  401_0_1_0")
        self.assertEqual(rg["rg_id"], "401_0_1_0")
        self.assertEqual(rg["rid"], "m54329_180927_232921/21627397/ccs")

    def test2_haplotig_iterator(self):
        in_fn = os.path.join(os.path.dirname(__file__), "data", "haplotig", "chr20.edge-map.tsv")
        haplotig_iter = lah.haplotig_iters.HaplotigIterator(in_fn)
        self.assertIsNotNone(haplotig_iter)

        haplotigs = []
        for h in haplotig_iter:
            haplotigs.append(h)

        self.assertEqual(len(haplotigs), 4)
        self.assertEqual(haplotigs[0]["rg_id"], "401_0_1_0")
        self.assertEqual(len(haplotigs[0]["rids"]), 1)
        self.assertEqual(haplotigs[1]["rg_id"], "401_0_2_0")
        self.assertEqual(len(haplotigs[1]["rids"]), 2)
        self.assertEqual(haplotigs[2]["rg_id"], "402_0_1_0")
        self.assertEqual(len(haplotigs[2]["rids"]), 8)
        self.assertEqual(haplotigs[3]["rg_id"], "402_0_2_0")
        self.assertEqual(len(haplotigs[3]["rids"]), 14)


# -- LahHaplotigItersTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
