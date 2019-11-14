import os, unittest

from .context import lah
import lah.haplotig_iters

class LahHaplotigItersTest(unittest.TestCase):

    def test1_validate_headers(self):
        with self.assertRaisesRegex(Exception, "Missing required headers: rid"):
            lah.haplotig_iters.HaplotigIterator.validate_headers(["NA", "READ", "hid"])

    def test2_haplotig_iterator(self):
        in_fn = os.path.join(os.path.dirname(__file__), "data", "haplotig", "chr20.edge-map.tsv")

        with self.assertRaisesRegex(Exception, "Missing required headers: rid"):
            lah.haplotig_iters.HaplotigIterator(headers=["NA", "READ", "hid"], in_fn=in_fn)

        haplotig_iter = lah.haplotig_iters.HaplotigIterator(headers=["NA", "rid", "hid"], in_fn=in_fn)
        self.assertIsNotNone(haplotig_iter)

        haplotigs = []
        for h in haplotig_iter:
            haplotigs.append(h)

        self.assertEqual(len(haplotigs), 4)
        self.assertEqual(haplotigs[0]["hid"], "401_0_1_0")
        self.assertEqual(len(haplotigs[0]["rids"]), 1)
        self.assertEqual(haplotigs[1]["hid"], "401_0_2_0")
        self.assertEqual(len(haplotigs[1]["rids"]), 2)
        self.assertEqual(haplotigs[2]["hid"], "402_0_1_0")
        self.assertEqual(len(haplotigs[2]["rids"]), 8)
        self.assertEqual(haplotigs[3]["hid"], "402_0_2_0")
        self.assertEqual(len(haplotigs[3]["rids"]), 14)


# -- LahHaplotigItersTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
