import os, tempfile, unittest

from .context import lah
from lah.haplotig import Haplotig
import lah.db

class LahHaplotigTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        self.dbfile = os.path.join(self.temp_d.name, "test.db")

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_haplotig_create_and_get(self):
        dbfile = self.dbfile
        db = lah.db.LahDb(dbfile=dbfile)
        db.create()
        sessionmaker = db.connect()
        session = sessionmaker()

        haplotig = Haplotig(name="402_0_2_0", reads_cnt=14, assembly_id=1)
        self.assertIsNotNone(haplotig)
        self.assertEqual(haplotig.name, "402_0_2_0")
        self.assertEqual(haplotig.reads_cnt, 14)

        session.add(haplotig)
        session.commit()

        self.assertEqual(haplotig.id, 1)
        haplotig = session.query(Haplotig).first()
        self.assertEqual(haplotig.id, 1)

# -- LahHaplotigTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
