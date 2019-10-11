import unittest

from .context import lah
import lah.edge_map

class LahEdgeMapTest(unittest.TestCase):
    start = ["chr1", 19248531, "G", "A", "a"]
    stop = ["chr1", 19255094, "T", "C", "a"]

    def test1_parse_chr(self):
        start_pos = "chr1:19248531_G_A_a"
        stop_pos = "chr1:19255094_T_C_a"

        chr_start = lah.edge_map.parse_chr_pos(start_pos)
        self.assertEqual(chr_start, self.start)
        chr_stop = lah.edge_map.parse_chr_pos(stop_pos)
        self.assertEqual(chr_stop, self.stop)

        chr_loc = lah.edge_map.parse_chr_loc( ";".join([start_pos, stop_pos]) )
        self.assertEqual(chr_loc, [self.start, self.stop])

    def test2_parse_edge_map(self):
        edge_map = lah.edge_map.parse_edge_map("ccs_1_4194529   @m54238_180901_011437/4194529/ccs   3   chr1:19248531_G_A_a;chr1:19255094_T_C_a")
        self.assertEqual(edge_map.hid, "3")
        self.assertEqual(edge_map.rid, "m54238_180901_011437/4194529/ccs")
        self.assertEqual(edge_map.start, self.start)
        self.assertEqual(edge_map.stop, self.stop)

# -- LahEdgeMapTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
