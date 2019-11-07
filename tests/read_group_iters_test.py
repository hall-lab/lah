import os, unittest

from .context import lah
import lah.read_group_iters

class LahReadGroupItersTest(unittest.TestCase):

    def test1_parse_line(self):
        rg = lah.read_group_iters.ReadGroupIterator.parse_line("ccs_31_21627397 @m54329_180927_232921/21627397/ccs  401_0_1_0")
        self.assertEqual(rg["rg_id"], "401_0_1_0")
        self.assertEqual(rg["rid"], "m54329_180927_232921/21627397/ccs")

    def test2_read_group_iterator(self):
        in_fn = os.path.join(os.path.dirname(__file__), "data", "read_group", "chr20.edge-map.tsv")
        read_group_iter = lah.read_group_iters.ReadGroupIterator(in_fn)
        self.assertIsNotNone(read_group_iter)

        read_groups = []
        for h in read_group_iter:
            read_groups.append(h)

        self.assertEqual(len(read_groups), 4)
        self.assertEqual(read_groups[0]["rg_id"], "401_0_1_0")
        self.assertEqual(len(read_groups[0]["rids"]), 1)
        self.assertEqual(read_groups[1]["rg_id"], "401_0_2_0")
        self.assertEqual(len(read_groups[1]["rids"]), 2)
        self.assertEqual(read_groups[2]["rg_id"], "402_0_1_0")
        self.assertEqual(len(read_groups[2]["rids"]), 8)
        self.assertEqual(read_groups[3]["rg_id"], "402_0_2_0")
        self.assertEqual(len(read_groups[3]["rids"]), 14)


# -- LahReadGroupItersTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
