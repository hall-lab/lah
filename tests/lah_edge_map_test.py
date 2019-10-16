import unittest

from .context import lah
import lah.edge_map

class LahEdgeMapTest(unittest.TestCase):

    def test1_parse_edge_map(self):
        edge_map = lah.edge_map.parse_edge_map("ccs_31_21627397 @m54329_180927_232921/21627397/ccs  401_0_1_0")
        self.assertEqual(edge_map.hid, "401_0_1_0")
        self.assertEqual(edge_map.rid, "m54329_180927_232921/21627397/ccs")

# -- LahEdgeMapTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
