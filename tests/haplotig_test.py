import os, tempfile, unittest

from .context import lah
from lah.haplotig import Haplotig, HaplotigRead
import lah.db

class LahHaplotigTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        self.dbfile = os.path.join(self.temp_d.name, "test.db")

    def tearDown(self):
        self.temp_d.cleanup()

    def test_haplotig_and_reads(self):
        dbfile = self.dbfile
        db = lah.db.LahDb(dbfile=dbfile)
        db.create()
        sessionmaker = db.connect()
        session = sessionmaker()

        hid = "402_0_2_0"
        haplotig = Haplotig(id=hid, sample_id=1)
        self.assertIsNotNone(haplotig)
        self.assertEqual(haplotig.id, hid)
        self.assertEqual(haplotig.length, None)

        session.add(haplotig)
        session.flush()
        self.assertEqual(haplotig.id, hid)

        session.commit()
        haplotig = session.query(Haplotig).first()
        self.assertEqual(haplotig.id, hid)

        rid = "m54238_180913_181445/44892801/ccs"
        rd = HaplotigRead(id=rid, haplotig_id=hid)
        self.assertIsNotNone(rd)
        self.assertEqual(rd.id, rid)
        self.assertEqual(rd.haplotig_id, hid)

        session.add(rd)
        session.flush()
        self.assertEqual(rd.id, rid)

        session.commit()
        rd = session.query(HaplotigRead).first()
        self.assertEqual(rd.id, rid)

        found_haplotig = rd.haplotig
        self.assertEqual(found_haplotig.id, hid)

        found_rds = found_haplotig.reads
        self.assertEqual(found_rds[0].id, rid)

# -- LahHaplotigTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
